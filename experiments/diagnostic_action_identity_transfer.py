"""Experiment 125: diagnostic frozen transfer with explicit action identity.

This hypothesis was motivated after observing Experiment 123/124 target results.
Therefore performance on 111-150 is diagnostic, not new prospective confirmation.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_111_150.csv")
OUT=Path("results/diagnostic_action_identity_transfer.csv")
BOOT=Path("results/diagnostic_action_identity_transfer_bootstrap.csv")
N_BOOT=5000
SEED=12544150

MODELS={
 "action_identity_only":["action_2","action_3"],
 "action_plus_context_support":["action_2","action_3","context_support_distance"],
 "action_plus_support_geometry":["action_2","action_3","context_support_distance","action_support_distance"],
 "action_plus_predicted_loss":["action_2","action_3","predicted_action_loss"],
 "action_plus_full_geometry":["action_2","action_3","context_support_distance","predicted_action_loss","action_support_distance"],
}


def prepare(path):
    d=pd.read_csv(path)
    d["action_2"]=(d["action"].astype(int)==2).astype(int)
    d["action_3"]=(d["action"].astype(int)==3).astype(int)
    req=sorted({x for v in MODELS.values() for x in v}|{"unsafe_action"})
    d=d.dropna(subset=req).copy()
    d["unsafe_action"]=d["unsafe_action"].astype(int)
    return d


def main():
    tr,te=prepare(TRAIN),prepare(TEST)
    yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
    preds={}; rows=[]
    for name,features in MODELS.items():
        m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=SEED))
        m.fit(tr[features],yt)
        p=m.predict_proba(te[features])[:,1]; z=(p>=.5).astype(int)
        preds[name]=p
        rows.append({"model":name,"features":"|".join(features),"train_rows":len(tr),"test_rows":len(te),
          "roc_auc":roc_auc_score(y,p),"balanced_accuracy_at_frozen_0_5":balanced_accuracy_score(y,z),
          "unsafe_recall_at_frozen_0_5":recall_score(y,z),
          "unsafe_precision_at_frozen_0_5":precision_score(y,z,zero_division=0)})
    rng=np.random.default_rng(SEED); safe=np.flatnonzero(y==0); unsafe=np.flatnonzero(y==1)
    vals={k:[] for k in MODELS}
    for _ in range(N_BOOT):
        idx=np.concatenate([rng.choice(safe,len(safe),replace=True),rng.choice(unsafe,len(unsafe),replace=True)])
        for name,p in preds.items(): vals[name].append(roc_auc_score(y[idx],p[idx]))
    br=[]
    base="action_identity_only"
    for name,v in vals.items():
        a=np.asarray(v)
        br.append({"contrast":name,"estimate":roc_auc_score(y,preds[name]),"ci_2_5":np.percentile(a,2.5),"ci_97_5":np.percentile(a,97.5),"probability_positive":""})
        if name!=base:
            diff=a-np.asarray(vals[base])
            br.append({"contrast":name+"_minus_"+base,"estimate":roc_auc_score(y,preds[name])-roc_auc_score(y,preds[base]),"ci_2_5":np.percentile(diff,2.5),"ci_97_5":np.percentile(diff,97.5),"probability_positive":np.mean(diff>0)})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT,index=False); pd.DataFrame(br).to_csv(BOOT,index=False)
    print(pd.DataFrame(rows).to_string(index=False)); print(pd.DataFrame(br).to_string(index=False))


if __name__=="__main__": main()
