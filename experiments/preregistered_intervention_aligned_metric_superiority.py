"""Experiment 162: preregistered intervention-aligned metric superiority."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path('results/action_conditioned_support_representation_analysis_actions_071_110.csv')
TEST=Path('results/prospective_action_conditioned_support_representation_actions_711_750.csv')
OUT=Path('results/preregistered_intervention_aligned_metric_superiority.csv')
SEED_OUT=Path('results/preregistered_intervention_aligned_metric_superiority_by_seed.csv')
FEATURES=['action_2','action_3','context_support_distance']
POISON_DOSE=0.20
SOURCE_UNSAFE_RECALL_TARGET=0.80
BOOT=10000
RNG_SEED=16244750

def prep(path):
    d=pd.read_csv(path).copy(); d['action_2']=(d.action.astype(int)==2).astype(int); d['action_3']=(d.action.astype(int)==3).astype(int); d['unsafe_action']=d.unsafe_action.astype(int)
    return d.dropna(subset=FEATURES+['unsafe_action','realized_action_regret','predicted_action_loss','generation_seed','test_index','action']).copy()

def fit(d,y):
    m=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',max_iter=5000,random_state=RNG_SEED)); m.fit(d[FEATURES],y); return m

def topn(scores,n):
    x=np.zeros(len(scores),bool); x[np.argsort(-scores,kind='stable')[:n]]=True; return x

def decisions(d,mask):
    tmp=d.assign(excluded=mask); unsafe=0; regret=0.0
    for _,g in tmp.groupby(['generation_seed','test_index'],sort=True):
        avail=np.flatnonzero(~g.excluded.to_numpy(bool));
        if len(avail)==0: avail=np.arange(len(g))
        losses=g.predicted_action_loss.to_numpy(float); actions=g.action.to_numpy(int)
        i=min(avail.tolist(),key=lambda j:(float(losses[j]),int(actions[j])))
        unsafe+=int(g.unsafe_action.to_numpy(int)[i]); regret+=float(g.realized_action_regret.to_numpy(float)[i])
    return unsafe,regret

def rho(a,b):
    r=spearmanr(a,b,nan_policy='omit').statistic
    return 0.0 if np.isnan(r) else float(r)

def main():
    tr=prep(TRAIN).reset_index(drop=True); te=prep(TEST).sort_values(['generation_seed','test_index','action']).reset_index(drop=True)
    clean=tr.unsafe_action.to_numpy(int); unsafe_idx=np.flatnonzero(clean==1)
    cm=fit(tr,clean); ss=cm.predict_proba(tr[FEATURES])[:,1]; su=np.sort(ss[clean==1]); thr=float(su[max(0,int(np.floor((1-SOURCE_UNSAFE_RECALL_TARGET)*len(su))))]); coverage=float(np.mean(ss>=thr))
    order=unsafe_idx[np.argsort(-tr.loc[unsafe_idx,'context_support_distance'].to_numpy(),kind='stable')]; n=max(1,int(round(POISON_DOSE*len(unsafe_idx)))); py=clean.copy(); py[order[:n]]=0; pm=fit(tr,py)
    rows=[]
    for seed,g in te.groupby('generation_seed',sort=True):
        g=g.reset_index(drop=True); y=g.unsafe_action.to_numpy(int); k=int(round(coverage*len(g))); cs=cm.predict_proba(g[FEATURES])[:,1]; ps=pm.predict_proba(g[FEATURES])[:,1]; ctop=topn(cs,k); ptop=topn(ps,k)
        cu,cr=decisions(g,ctop); pu,pr=decisions(g,ptop)
        rows.append({'generation_seed':seed,'delta_auc':roc_auc_score(y,ps)-roc_auc_score(y,cs),'delta_ap':average_precision_score(y,ps)-average_precision_score(y,cs),'delta_recall':float(y[ptop].sum()/max(1,y.sum())-y[ctop].sum()/max(1,y.sum())),'delta_unsafe':pu-cu,'delta_regret':pr-cr})
    s=pd.DataFrame(rows); r_recall=rho(s.delta_recall,s.delta_unsafe); r_auc=rho(s.delta_auc,s.delta_unsafe); r_ap=rho(s.delta_ap,s.delta_unsafe)
    obs_ra=abs(r_recall)-abs(r_auc); obs_rp=abs(r_recall)-abs(r_ap)
    rng=np.random.default_rng(RNG_SEED); dra=[]; drp=[]; idx=np.arange(len(s))
    for _ in range(BOOT):
        b=rng.choice(idx,size=len(idx),replace=True); sb=s.iloc[b]
        rr=abs(rho(sb.delta_recall,sb.delta_unsafe)); ra=abs(rho(sb.delta_auc,sb.delta_unsafe)); rp=abs(rho(sb.delta_ap,sb.delta_unsafe)); dra.append(rr-ra); drp.append(rr-rp)
    ci_ra=np.percentile(dra,[2.5,97.5]); ci_rp=np.percentile(drp,[2.5,97.5])
    row={'seeds':len(s),'rho_recall_unsafe':r_recall,'rho_auc_unsafe':r_auc,'rho_ap_unsafe':r_ap,'absdiff_recall_minus_auc':obs_ra,'absdiff_recall_minus_ap':obs_rp,'boot_recall_minus_auc_p025':ci_ra[0],'boot_recall_minus_auc_p975':ci_ra[1],'boot_recall_minus_ap_p025':ci_rp[0],'boot_recall_minus_ap_p975':ci_rp[1],'criterion_observed_superiority':int(abs(r_recall)>abs(r_auc) and abs(r_recall)>abs(r_ap)),'criterion_boot_auc_above_zero':int(ci_ra[0]>0),'criterion_boot_ap_above_zero':int(ci_rp[0]>0)}
    row['primary_metric_superiority_pass']=int(row['criterion_observed_superiority'] and row['criterion_boot_auc_above_zero'] and row['criterion_boot_ap_above_zero'])
    row['rho_recall_regret']=rho(s.delta_recall,s.delta_regret); row['rho_auc_regret']=rho(s.delta_auc,s.delta_regret); row['rho_ap_regret']=rho(s.delta_ap,s.delta_regret)
    OUT.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame([row]).to_csv(OUT,index=False); s.to_csv(SEED_OUT,index=False); print(pd.DataFrame([row]).to_string(index=False))

if __name__=='__main__': main()
