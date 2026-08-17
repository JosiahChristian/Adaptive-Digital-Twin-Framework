"""Experiment 134: preregistered sixth-population unlabeled-EM confirmation."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss,log_loss,roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_231_270.csv")
OUT=Path("results/preregistered_sixth_population_unlabeled_em.csv")
FEATURES=["action_2","action_3","context_support_distance"]
def prep(path):
 d=pd.read_csv(path); d["action_2"]=(d.action.astype(int)==2).astype(int); d["action_3"]=(d.action.astype(int)==3).astype(int); d["unsafe_action"]=d.unsafe_action.astype(int)
 return d.dropna(subset=FEATURES+["unsafe_action"]).copy()
def logit(p):
 p=np.clip(p,1e-9,1-1e-9); return np.log(p/(1-p))
def sigmoid(x): return 1/(1+np.exp(-x))
def ece(y,p,bins=10):
 edges=np.linspace(0,1,bins+1); z=np.clip(np.digitize(p,edges[1:-1]),0,bins-1)
 return float(sum((z==b).mean()*abs(y[z==b].mean()-p[z==b].mean()) for b in range(bins) if np.any(z==b)))
def adapt(q,pi,max_iter=1000,tol=1e-10):
 t=pi
 for i in range(max_iter):
  p=sigmoid(logit(q)+np.log(t/(1-t))-np.log(pi/(1-pi))); u=float(p.mean())
  if abs(u-t)<tol:return p,u,i+1
  t=np.clip(u,1e-6,1-1e-6)
 return p,t,max_iter
def main():
 tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy(); pi=yt.mean()
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=13444270)); m.fit(tr[FEATURES],yt)
 raw=m.predict_proba(te[FEATURES])[:,1]; fixed=sigmoid(logit(raw)+np.log(pi/(1-pi))); em,epi,n=adapt(fixed,pi)
 rows=[]
 for name,p,assumed in [("primary_unlabeled_em",em,epi),("comparator_fixed_source_prior",fixed,pi)]:
  rows.append({"model":name,"source_prior":pi,"estimated_or_assumed_prior":assumed,"em_iterations":n if name.startswith("primary") else 0,
   "test_rows":len(te),"test_unsafe":int(y.sum()),"test_prevalence":y.mean(),"mean_predicted_risk":p.mean(),
   "absolute_mean_risk_error":abs(p.mean()-y.mean()),"roc_auc":roc_auc_score(y,p),"brier_score":brier_score_loss(y,p),
   "log_loss":log_loss(y,p),"ece_10_equal_width":ece(y,p)})
 OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(OUT,index=False); print(pd.DataFrame(rows).to_string(index=False))
if __name__=="__main__":main()
