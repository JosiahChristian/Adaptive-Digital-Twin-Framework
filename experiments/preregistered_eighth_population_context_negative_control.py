"""Experiment 140: preregistered eighth-population context-value confirmation."""
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_311_350.csv")
OUT=Path("results/preregistered_eighth_population_context_negative_control.csv")
TRIALS=Path("results/preregistered_eighth_population_matched_random_trials.csv")
F=["action_2","action_3","context_support_distance"]; R=.80; N=5000; SEED=14044350
def prep(path):
 d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int); d["unsafe_action"]=d.unsafe_action.astype(int)
 return d.dropna(subset=F+["unsafe_action"]).copy()
def met(y,z):
 tn,fp,fn,tp=confusion_matrix(y,z,labels=[0,1]).ravel()
 return {"unsafe_recall":tp/(tp+fn),"unsafe_precision":tp/(tp+fp),"balanced_accuracy":.5*(tp/(tp+fn)+tn/(tn+fp)),"true_positives":tp,"alert_coverage":z.mean()}
def main():
 tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=SEED)); m.fit(tr[F],yt)
 ss=m.predict_proba(tr[F])[:,1]; ts=m.predict_proba(te[F])[:,1]; us=np.sort(ss[yt==1]); st=float(us[max(0,int(np.floor((1-R)*len(us))))]); cov=float(np.mean(ss>=st))
 tt=float(np.quantile(ts,1-cov,method="higher")); primary=(ts>=tt).astype(int); pm=met(y,primary)
 action1=(te.action.astype(int).to_numpy()==1).astype(int); extra=int(primary.sum()-action1.sum()); pool=np.flatnonzero(action1==0); rng=np.random.default_rng(SEED); rows=[]
 for i in range(N):
  z=action1.copy(); z[rng.choice(pool,extra,replace=False)]=1; rows.append({"trial":i+1,**met(y,z)})
 td=pd.DataFrame(rows); out={"test_rows":len(te),"test_unsafe":int(y.sum()),"test_prevalence":y.mean(),"frozen_source_coverage":cov,"target_threshold":tt,**pm}
 for k in ["unsafe_recall","unsafe_precision","balanced_accuracy","true_positives"]:
  v=td[k].to_numpy(); out["random_"+k+"_mean"]=v.mean(); out["random_"+k+"_ci_2_5"]=np.percentile(v,2.5); out["random_"+k+"_ci_97_5"]=np.percentile(v,97.5)
  out["primary_minus_random_"+k+"_mean"]=pm[k]-v.mean(); out["probability_random_ge_primary_"+k]=np.mean(v>=pm[k])
 out["criterion_recall_above_random_97_5"]=int(pm["unsafe_recall"]>out["random_unsafe_recall_ci_97_5"])
 out["criterion_balanced_accuracy_above_random_97_5"]=int(pm["balanced_accuracy"]>out["random_balanced_accuracy_ci_97_5"])
 out["criterion_true_positives_above_random_97_5"]=int(pm["true_positives"]>out["random_true_positives_ci_97_5"])
 out["all_primary_criteria_pass"]=int(all(out[k] for k in ["criterion_recall_above_random_97_5","criterion_balanced_accuracy_above_random_97_5","criterion_true_positives_above_random_97_5"]))
 OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame([out]).to_csv(OUT,index=False); td.to_csv(TRIALS,index=False); print(pd.DataFrame([out]).to_string(index=False))
if __name__=="__main__":main()
