"""Experiment 137: preregistered seventh-population fixed-coverage alert rule."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_271_310.csv")
OUT=Path("results/preregistered_seventh_population_fixed_coverage_alert.csv")
ACTION_OUT=Path("results/preregistered_seventh_population_fixed_coverage_alert_by_action.csv")
BOOT_OUT=Path("results/preregistered_seventh_population_fixed_coverage_alert_cluster_bootstrap.csv")
FEATURES=["action_2","action_3","context_support_distance"]; TARGET_RECALL=.80; N_BOOT=5000; SEED=13744310
def prep(path):
 d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int); d["unsafe_action"]=d.unsafe_action.astype(int)
 return d.dropna(subset=FEATURES+["unsafe_action","generation_seed"]).copy()
def met(y,z):
 tn,fp,fn,tp=confusion_matrix(y,z,labels=[0,1]).ravel()
 return {"unsafe_recall":tp/(tp+fn),"safe_specificity":tn/(tn+fp),"unsafe_precision":tp/(tp+fp),"negative_predictive_value":tn/(tn+fn),
 "alert_coverage":z.mean(),"balanced_accuracy":.5*(tp/(tp+fn)+tn/(tn+fp))}
def main():
 tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=SEED)); m.fit(tr[FEATURES],yt)
 ss=m.predict_proba(tr[FEATURES])[:,1]; ts=m.predict_proba(te[FEATURES])[:,1]
 us=np.sort(ss[yt==1]); idx=max(0,int(np.floor((1-TARGET_RECALL)*len(us)))); source_threshold=float(us[idx]); coverage=float(np.mean(ss>=source_threshold))
 threshold=float(np.quantile(ts,1-coverage,method="higher")); z=(ts>=threshold).astype(int); metrics=met(y,z)
 row={"rule":"unlabeled_fixed_coverage","train_rows":len(tr),"test_rows":len(te),"test_unsafe":int(y.sum()),"test_prevalence":y.mean(),
 "source_threshold":source_threshold,"frozen_source_coverage":coverage,"target_quantile_threshold":threshold,"roc_auc":roc_auc_score(y,ts),**metrics}
 row.update({"criterion_recall_ge_0_75":int(metrics["unsafe_recall"]>=.75),"criterion_npv_ge_0_90":int(metrics["negative_predictive_value"]>=.90),
 "criterion_coverage_within_0_01":int(abs(metrics["alert_coverage"]-coverage)<=.01)})
 row["all_primary_criteria_pass"]=int(all(row[k] for k in ["criterion_recall_ge_0_75","criterion_npv_ge_0_90","criterion_coverage_within_0_01"]))
 actions=[]
 for action,g in te.assign(alert=z).groupby("action"):
  gy=g.unsafe_action.to_numpy(); gz=g.alert.to_numpy()
  actions.append({"action":int(action),"rows":len(g),"unsafe_rows":int(gy.sum()),"unsafe_prevalence":gy.mean(),"alert_coverage":gz.mean(),
  "unsafe_recall":gz[gy==1].mean() if gy.sum() else np.nan,"unsafe_precision":gy[gz==1].mean() if gz.sum() else 0})
 seeds=np.sort(te.generation_seed.unique()); rng=np.random.default_rng(SEED); br=[]
 for i in range(N_BOOT):
  chosen=rng.choice(seeds,len(seeds),replace=True); bi=np.concatenate([np.flatnonzero(te.generation_seed.to_numpy()==s) for s in chosen])
  bm=met(y[bi],z[bi]); br.append({"bootstrap":i+1,**bm})
 bd=pd.DataFrame(br)
 for key in ["unsafe_recall","negative_predictive_value","balanced_accuracy"]:
  row[key+"_cluster_ci_2_5"]=np.percentile(bd[key],2.5); row[key+"_cluster_ci_97_5"]=np.percentile(bd[key],97.5)
 OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame([row]).to_csv(OUT,index=False); pd.DataFrame(actions).to_csv(ACTION_OUT,index=False); bd.to_csv(BOOT_OUT,index=False)
 print(pd.DataFrame([row]).to_string(index=False)); print(pd.DataFrame(actions).to_string(index=False))
if __name__=="__main__":main()
