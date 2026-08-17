"""Experiment 135: conservative alert-rule stability across populations.

A source-only threshold is chosen as the highest threshold attaining at least
80% unsafe recall on population 071-110. Its source alert coverage is then
frozen. Two deployment rules are compared on four exposed populations:
(1) the fixed source score threshold and (2) an unlabeled target quantile that
preserves only the frozen alert coverage. This is diagnostic; the selected rule
requires a new prospective population.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TARGETS={
 "third_111_150":Path("results/prospective_action_conditioned_support_representation_actions_111_150.csv"),
 "fourth_151_190":Path("results/prospective_action_conditioned_support_representation_actions_151_190.csv"),
 "fifth_191_230":Path("results/prospective_action_conditioned_support_representation_actions_191_230.csv"),
 "sixth_231_270":Path("results/prospective_action_conditioned_support_representation_actions_231_270.csv"),
}
OUT=Path("results/conservative_alert_rule_stability.csv")
BY_ACTION=Path("results/conservative_alert_rule_stability_by_action.csv")
FEATURES=["action_2","action_3","context_support_distance"]
TARGET_RECALL=0.80

def prep(path):
 d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int); d["unsafe_action"]=d.unsafe_action.astype(int)
 return d.dropna(subset=FEATURES+["unsafe_action"]).copy()

def metrics(y,pred):
 tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
 return {"unsafe_recall":tp/(tp+fn),"safe_specificity":tn/(tn+fp),"unsafe_precision":tp/(tp+fp) if tp+fp else 0,
 "negative_predictive_value":tn/(tn+fn) if tn+fn else 0,"alert_coverage":pred.mean(),"balanced_accuracy":.5*(tp/(tp+fn)+tn/(tn+fp)),
 "tp":tp,"fp":fp,"tn":tn,"fn":fn}

def main():
 tr=prep(TRAIN); yt=tr.unsafe_action.to_numpy()
 model=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=135))
 model.fit(tr[FEATURES],yt); source_score=model.predict_proba(tr[FEATURES])[:,1]
 unsafe_scores=np.sort(source_score[yt==1])
 index=max(0,int(np.floor((1-TARGET_RECALL)*len(unsafe_scores))))
 source_threshold=float(unsafe_scores[index])
 source_coverage=float(np.mean(source_score>=source_threshold))
 rows=[]; action_rows=[]
 for population,path in TARGETS.items():
  d=prep(path); y=d.unsafe_action.to_numpy(); score=model.predict_proba(d[FEATURES])[:,1]
  rules={"fixed_source_threshold":source_threshold,
         "unlabeled_fixed_coverage":float(np.quantile(score,1-source_coverage,method="higher"))}
  for rule,threshold in rules.items():
   pred=(score>=threshold).astype(int); row={"population":population,"rule":rule,"rows":len(d),"unsafe_rows":int(y.sum()),
    "unsafe_prevalence":y.mean(),"roc_auc":roc_auc_score(y,score),"source_threshold":source_threshold,
    "applied_threshold":threshold,"frozen_source_coverage":source_coverage}; row.update(metrics(y,pred)); rows.append(row)
   for action,g in d.assign(pred=pred).groupby("action"):
    gy=g.unsafe_action.to_numpy(); gp=g.pred.to_numpy()
    action_rows.append({"population":population,"rule":rule,"action":int(action),"rows":len(g),"unsafe_rows":int(gy.sum()),
      "unsafe_prevalence":gy.mean(),"alert_coverage":gp.mean(),"unsafe_recall":gp[gy==1].mean() if gy.sum() else np.nan,
      "unsafe_precision":gy[gp==1].mean() if gp.sum() else 0})
 OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(OUT,index=False); pd.DataFrame(action_rows).to_csv(BY_ACTION,index=False)
 print("source_threshold",source_threshold,"source_coverage",source_coverage)
 print(pd.DataFrame(rows).to_string(index=False))

if __name__=="__main__":main()
