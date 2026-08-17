"""Experiment 138: action-identity negative control for Experiment 137."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_271_310.csv")
OUT=Path("results/action_identity_matched_coverage_negative_control.csv")
RANDOM_OUT=Path("results/action_identity_matched_coverage_random_trials.csv")
FEATURES=["action_2","action_3","context_support_distance"]; TARGET_RECALL=.80; N=5000; SEED=13844310
def prep(path):
 d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int); d["unsafe_action"]=d.unsafe_action.astype(int)
 return d.dropna(subset=FEATURES+["unsafe_action"]).copy()
def met(y,z):
 tn,fp,fn,tp=confusion_matrix(y,z,labels=[0,1]).ravel()
 return {"unsafe_recall":tp/(tp+fn),"safe_specificity":tn/(tn+fp),"unsafe_precision":tp/(tp+fp) if tp+fp else 0,
 "negative_predictive_value":tn/(tn+fn),"alert_coverage":z.mean(),"balanced_accuracy":.5*(tp/(tp+fn)+tn/(tn+fp)),"true_positives":tp}
def main():
 tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=SEED)); m.fit(tr[FEATURES],yt)
 ss=m.predict_proba(tr[FEATURES])[:,1]; ts=m.predict_proba(te[FEATURES])[:,1]; us=np.sort(ss[yt==1])
 threshold=float(us[max(0,int(np.floor((1-TARGET_RECALL)*len(us))))]); coverage=float(np.mean(ss>=threshold))
 target_threshold=float(np.quantile(ts,1-coverage,method="higher")); primary=(ts>=target_threshold).astype(int)
 action1=(te.action.astype(int).to_numpy()==1).astype(int); target_alerts=int(primary.sum()); extra=target_alerts-int(action1.sum())
 pool=np.flatnonzero(action1==0); rng=np.random.default_rng(SEED); trials=[]
 for i in range(N):
  z=action1.copy(); z[rng.choice(pool,extra,replace=False)]=1; trials.append({"trial":i+1,**met(y,z)})
 td=pd.DataFrame(trials); pm=met(y,primary); am=met(y,action1)
 rows=[{"policy":"primary_context_ranked_fixed_coverage",**pm},{"policy":"action_1_only",**am}]
 for metric in ["unsafe_recall","unsafe_precision","balanced_accuracy","true_positives"]:
  v=td[metric].to_numpy(); rows.append({"policy":"matched_random_"+metric,"unsafe_recall":np.nan,"safe_specificity":np.nan,
   "unsafe_precision":np.nan,"negative_predictive_value":np.nan,"alert_coverage":coverage,"balanced_accuracy":np.nan,
   "true_positives":np.nan,"random_metric":metric,"random_mean":v.mean(),"random_ci_2_5":np.percentile(v,2.5),
   "random_ci_97_5":np.percentile(v,97.5),"primary_minus_random_mean":pm[metric]-v.mean(),
   "probability_random_ge_primary":np.mean(v>=pm[metric])})
 OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(OUT,index=False); td.to_csv(RANDOM_OUT,index=False)
 print(pd.DataFrame(rows).to_string(index=False))
if __name__=="__main__":main()
