"""Experiment 132: unlabeled target-prior adaptation diagnostic.

EM uses only target feature scores, never target unsafe labels. Evaluation labels
are opened only after the adapted probabilities are frozen.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_191_230.csv")
OUT=Path("results/unlabeled_target_prior_adaptation_diagnostic.csv")
TRACE=Path("results/unlabeled_target_prior_adaptation_trace.csv")
FEATURES=["action_2","action_3","context_support_distance"]

def prep(path):
    d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int)
    d["unsafe_action"]=d.unsafe_action.astype(int); return d.dropna(subset=FEATURES+["unsafe_action"]).copy()

def logit(p):
    p=np.clip(p,1e-9,1-1e-9); return np.log(p/(1-p))

def sigmoid(x): return 1/(1+np.exp(-x))

def ece(y,p,bins=10):
    edges=np.linspace(0,1,bins+1); z=np.clip(np.digitize(p,edges[1:-1]),0,bins-1)
    return float(sum((z==b).mean()*abs(y[z==b].mean()-p[z==b].mean()) for b in range(bins) if np.any(z==b)))

def em_prior(q,source_prior,max_iter=1000,tol=1e-10):
    target_prior=source_prior; trace=[]
    for i in range(max_iter):
        shift=np.log(target_prior/(1-target_prior))-np.log(source_prior/(1-source_prior))
        p=sigmoid(logit(q)+shift); updated=float(p.mean())
        trace.append({"iteration":i+1,"target_prior":target_prior,"updated_prior":updated,"absolute_change":abs(updated-target_prior)})
        if abs(updated-target_prior)<tol: return p,updated,trace
        target_prior=np.clip(updated,1e-6,1-1e-6)
    return p,target_prior,trace

def main():
    tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy(); source_prior=yt.mean()
    m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=13244230))
    m.fit(tr[FEATURES],yt); raw=m.predict_proba(te[FEATURES])[:,1]
    q=sigmoid(logit(raw)+np.log(source_prior/(1-source_prior)))
    adapted,estimated_prior,trace=em_prior(q,source_prior)
    rows=[]
    for name,p in {"fixed_source_prior":q,"unlabeled_em_target_prior":adapted}.items():
        rows.append({"model":name,"source_prior":source_prior,"estimated_target_prior":estimated_prior if name.startswith("unlabeled") else source_prior,
          "observed_target_prevalence":y.mean(),"mean_predicted_risk":p.mean(),"absolute_mean_risk_error":abs(p.mean()-y.mean()),
          "roc_auc":roc_auc_score(y,p),"brier_score":brier_score_loss(y,p),"log_loss":log_loss(y,p),"ece_10_equal_width":ece(y,p)})
    OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(OUT,index=False); pd.DataFrame(trace).to_csv(TRACE,index=False)
    print(pd.DataFrame(rows).to_string(index=False)); print("iterations",len(trace))

if __name__=="__main__": main()
