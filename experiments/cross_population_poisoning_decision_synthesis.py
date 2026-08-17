"""Experiment 159: retrospective cross-population synthesis.

Applies the same clean model, 20% targeted unsafe-to-safe source-label concealment,
and fixed clean-derived coverage rule to four untouched prospective populations.
This is descriptive synthesis, not a new prospective test.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path('results/action_conditioned_support_representation_analysis_actions_071_110.csv')
BLOCKS=[('511_550','results/prospective_action_conditioned_support_representation_actions_511_550.csv'),('551_590','results/prospective_action_conditioned_support_representation_actions_551_590.csv'),('591_630','results/prospective_action_conditioned_support_representation_actions_591_630.csv'),('631_670','results/prospective_action_conditioned_support_representation_actions_631_670.csv')]
OUT=Path('results/cross_population_poisoning_decision_synthesis.csv')
FEATURES=['action_2','action_3','context_support_distance']
RNG=15944670

def prep(path):
 d=pd.read_csv(path).copy(); d['action_2']=(d.action.astype(int)==2).astype(int); d['action_3']=(d.action.astype(int)==3).astype(int); d['unsafe_action']=d.unsafe_action.astype(int); return d.dropna(subset=FEATURES+['unsafe_action','realized_action_regret','predicted_action_loss','generation_seed','test_index','action']).copy()
def fit(d,y):
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',max_iter=5000,random_state=RNG)); m.fit(d[FEATURES],y); return m
def mask(scores,n):
 z=np.zeros(len(scores),bool); z[np.argsort(-scores,kind='stable')[:n]]=True; return z
def evaluate(te,m,n):
 scores=m.predict_proba(te[FEATURES])[:,1]; ex=mask(scores,n); tmp=te.assign(ex=ex); u=0; r=0.0; c=0
 for _,g in tmp.groupby(['generation_seed','test_index'],sort=True):
  avail=np.flatnonzero(~g.ex.to_numpy(bool)); avail=avail if len(avail) else np.arange(len(g)); losses=g.predicted_action_loss.to_numpy(float); acts=g.action.to_numpy(int); i=int(min(avail.tolist(),key=lambda j:(float(losses[j]),int(acts[j])))); u+=int(g.unsafe_action.to_numpy(int)[i]); r+=float(g.realized_action_regret.to_numpy(float)[i]); c+=1
 y=te.unsafe_action.to_numpy(int); return scores,u,r,c,float(roc_auc_score(y,scores)),float(average_precision_score(y,scores)),float(y[ex].sum()/max(1,y.sum()))
def main():
 tr=prep(TRAIN).reset_index(drop=True); y=tr.unsafe_action.to_numpy(int); clean=fit(tr,y); src=clean.predict_proba(tr[FEATURES])[:,1]; unsafe=np.flatnonzero(y==1); order=unsafe[np.argsort(-tr.loc[unsafe,'context_support_distance'].to_numpy(),kind='stable')]; pn=int(round(.20*len(unsafe))); py=y.copy(); py[order[:pn]]=0; poison=fit(tr,py)
 sus=np.sort(src[y==1]); th=float(sus[max(0,int(np.floor(.20*len(sus))))]); coverage=float(np.mean(src>=th)); rows=[]
 for name,path in BLOCKS:
  te=prep(Path(path)).sort_values(['generation_seed','test_index','action'],kind='stable').reset_index(drop=True); n=int(round(coverage*len(te))); cs,cu,cr,c,ca,cap,crec=evaluate(te,clean,n); ps,pu,pr,_,pa,pap,prec=evaluate(te,poison,n)
  rows.append({'block':name,'contexts':c,'delta_auc_poison_minus_clean':pa-ca,'delta_ap':pap-cap,'delta_excluded_unsafe_recall':prec-crec,'delta_unsafe_selected':pu-cu,'delta_regret':pr-cr,'clean_unsafe_selected':cu,'poison_unsafe_selected':pu,'clean_regret':cr,'poison_regret':pr})
 df=pd.DataFrame(rows); df.to_csv(OUT,index=False); print(df.to_string(index=False)); print('\nSign counts:'); print({'poison_better_unsafe':int((df.delta_unsafe_selected<0).sum()),'poison_worse_unsafe':int((df.delta_unsafe_selected>0).sum()),'poison_better_regret':int((df.delta_regret<0).sum()),'poison_worse_regret':int((df.delta_regret>0).sum()),'auc_improves':int((df.delta_auc_poison_minus_clean>0).sum()),'auc_degrades':int((df.delta_auc_poison_minus_clean<0).sum())})
if __name__=='__main__': main()
