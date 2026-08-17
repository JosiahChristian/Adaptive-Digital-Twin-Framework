"""Experiment 129: source-only probability calibration diagnostics.

All estimators fit only population 071-110. Population 151-190 is evaluation
only. Selection based on this diagnostic requires a new prospective population.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_151_190.csv")
OUT=Path("results/source_only_probability_calibration_diagnostic.csv")
BINS=Path("results/source_only_probability_calibration_bins.csv")
FEATURES=["action_2","action_3","context_support_distance"]


def prep(path):
    d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int)
    d["unsafe_action"]=d.unsafe_action.astype(int); return d.dropna(subset=FEATURES+["unsafe_action"]).copy()


def logit(p):
    p=np.clip(p,1e-9,1-1e-9); return np.log(p/(1-p))


def sigmoid(x):
    return 1/(1+np.exp(-x))


def ece(y,p,bins=10):
    edges=np.linspace(0,1,bins+1); z=np.clip(np.digitize(p,edges[1:-1]),0,bins-1)
    return float(sum((z==b).mean()*abs(y[z==b].mean()-p[z==b].mean()) for b in range(bins) if np.any(z==b)))


def main():
    tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
    preds={}
    for name,weight in [("balanced_logistic","balanced"),("unweighted_logistic",None)]:
        m=make_pipeline(StandardScaler(),LogisticRegression(class_weight=weight,max_iter=5000,random_state=12944190))
        m.fit(tr[FEATURES],yt); preds[name]=m.predict_proba(te[FEATURES])[:,1]
    source_prior=yt.mean()
    preds["balanced_source_prior_corrected"]=sigmoid(logit(preds["balanced_logistic"])+np.log(source_prior/(1-source_prior)))
    rows=[]; bins=[]
    for name,p in preds.items():
        rows.append({"model":name,"train_prevalence":yt.mean(),"test_prevalence":y.mean(),"mean_predicted_risk":p.mean(),
          "roc_auc":roc_auc_score(y,p),"brier_score":brier_score_loss(y,p),"log_loss":log_loss(y,p),
          "ece_10_equal_width":ece(y,p),"balanced_accuracy_at_0_5":balanced_accuracy_score(y,p>=.5)})
        q=pd.qcut(p,q=10,duplicates="drop")
        for i,(_,g) in enumerate(pd.DataFrame({"y":y,"p":p,"q":q}).groupby("q",observed=True),1):
            bins.append({"model":name,"quantile_bin":i,"rows":len(g),"mean_predicted_risk":g.p.mean(),"observed_unsafe_fraction":g.y.mean()})
    OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(OUT,index=False); pd.DataFrame(bins).to_csv(BINS,index=False)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__=="__main__": main()
