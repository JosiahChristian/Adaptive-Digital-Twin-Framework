"""Stronger preregistered label-preserving control for Experiment 166."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path('results/action_conditioned_support_representation_analysis_actions_071_110.csv')
TEST=Path('results/prospective_action_conditioned_support_representation_actions_791_830.csv')
OUTDIR=Path('results/audit/experiment_166_stronger_label_preserving_control')
FEATURES=['action_2','action_3','context_support_distance']
RNG_SEED=16644830; POISON_DOSE=0.20; SOURCE_UNSAFE_RECALL_TARGET=0.80; PRIMARY_BAND=0.10
TARGET_SEEDS=list(range(44791,44831)); BOOT=10000; PRIMARY_BOOT_SEED=16658001; SECONDARY_BOOT_SEED=16658002
SIGMAS=[0.05,0.10,0.15,0.20,0.30,0.40,0.55,0.70,0.90,1.10,1.40,1.80,2.30,3.00,4.00,5.50]
REPS=16; N_CAND=len(SIGMAS)*REPS; CAND_SEED0=16657000
HIST_TOTAL_SWITCHES=308; HIST_MEAN_JACCARD=0.9238228511679869

def prep(path):
 d=pd.read_csv(path).copy(); d['action_2']=(d.action.astype(int)==2).astype(int); d['action_3']=(d.action.astype(int)==3).astype(int); d['unsafe_action']=d.unsafe_action.astype(int)
 return d.dropna(subset=FEATURES+['unsafe_action','realized_action_regret','predicted_action_loss','generation_seed','test_index','action']).copy()

def fit(d,y):
 m=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',max_iter=5000,random_state=RNG_SEED)); m.fit(d[FEATURES],y); return m

def topn(scores,n):
 mask=np.zeros(len(scores),bool); mask[np.argsort(-scores,kind='stable')[:n]]=True; return mask

def select_actions(g,excluded):
 tmp=g.assign(excluded=np.asarray(excluded,bool)); out=[]
 for (seed,idx),c in tmp.groupby(['generation_seed','test_index'],sort=True):
  c=c.reset_index(drop=True); avail=np.flatnonzero(~c.excluded.to_numpy(bool)); avail=np.arange(len(c)) if len(avail)==0 else avail
  losses=c.predicted_action_loss.to_numpy(float); actions=c.action.to_numpy(int); j=min(avail.tolist(),key=lambda i:(float(losses[i]),int(actions[i])))
  out.append((int(seed),int(idx),int(actions[j]),int(c.unsafe_action.iloc[j]),float(c.realized_action_regret.iloc[j])))
 return pd.DataFrame(out,columns=['generation_seed','test_index','action','unsafe_action','realized_action_regret'])

def seed_geometry(te,clean,alt,coverage):
 rows=[]
 for seed,g0 in te.groupby('generation_seed',sort=True):
  g=g0.reset_index(drop=True); k=int(round(coverage*len(g))); cs=clean.predict_proba(g[FEATURES])[:,1]; xs=alt.predict_proba(g[FEATURES])[:,1]
  cm=topn(cs,k); xm=topn(xs,k); cutoff=float(np.min(cs[cm])); margin=np.abs(cs-cutoff); band_n=max(1,int(np.ceil(PRIMARY_BAND*len(g)))); near=np.zeros(len(g),bool); near[np.argsort(margin,kind='stable')[:band_n]]=True
  sw=cm^xm; inter=int(np.sum(cm&xm)); union=int(np.sum(cm|xm)); nr=float(np.sum(sw&near)/max(1,np.sum(near))); fr=float(np.sum(sw&~near)/max(1,np.sum(~near)))
  csel=select_actions(g,cm); xsel=select_actions(g,xm); mer=csel.merge(xsel,on=['generation_seed','test_index'],suffixes=('_clean','_alt'))
  rows.append({'generation_seed':int(seed),'membership_switches':int(sw.sum()),'exclusion_jaccard':inter/union if union else 1.0,'near_switches':int(np.sum(sw&near)),'far_switches':int(np.sum(sw&~near)),'near_rows':int(np.sum(near)),'far_rows':int(np.sum(~near)),'near_switch_rate':nr,'far_switch_rate':fr,'D_near_minus_far':nr-fr,'selected_action_changes':int(np.sum(mer.action_clean!=mer.action_alt)),'delta_unsafe_selected':int(mer.unsafe_action_alt.sum()-mer.unsafe_action_clean.sum()),'delta_total_regret':float(mer.realized_action_regret_alt.sum()-mer.realized_action_regret_clean.sum()),'mean_abs_score_shift':float(np.mean(np.abs(xs-cs)))})
 return pd.DataFrame(rows)

def boot_mean(v,seed):
 rng=np.random.default_rng(seed); v=np.asarray(v,float); n=len(v); out=np.empty(BOOT,float)
 for i in range(BOOT): out[i]=float(np.mean(v[rng.integers(0,n,size=n)]))
 return np.percentile(out,[2.5,97.5])

def main():
 tr=prep(TRAIN).reset_index(drop=True); te=prep(TEST).sort_values(['generation_seed','test_index','action']).reset_index(drop=True)
 assert sorted(te.generation_seed.unique().astype(int).tolist())==TARGET_SEEDS; assert (te.groupby(['generation_seed','test_index']).size()==3).all()
 y0=tr.unsafe_action.to_numpy(int); unsafe_idx=np.flatnonzero(y0==1); clean=fit(tr,y0); source_scores=clean.predict_proba(tr[FEATURES])[:,1]
 source_unsafe=np.sort(source_scores[y0==1]); q=max(0,int(np.floor((1-SOURCE_UNSAFE_RECALL_TARGET)*len(source_unsafe)))); threshold=float(source_unsafe[q]); coverage=float(np.mean(source_scores>=threshold))
 poison_order=unsafe_idx[np.argsort(-tr.loc[unsafe_idx,'context_support_distance'].to_numpy(),kind='stable')]; poison_n=max(1,int(round(POISON_DOSE*len(unsafe_idx)))); py=y0.copy(); py[poison_order[:poison_n]]=0; poison=fit(tr,py)
 pseed=seed_geometry(te,clean,poison,coverage); hist_j=float(pseed.exclusion_jaccard.mean()); hist_sw=int(pseed.membership_switches.sum())
 if hist_sw!=HIST_TOTAL_SWITCHES or not np.isclose(hist_j,HIST_MEAN_JACCARD,rtol=0,atol=1e-12): raise RuntimeError(f'historical mismatch {hist_sw} {hist_j}')
 scale=float(tr.context_support_distance.std(ddof=0)); diagnostics=[]; models=[]
 for j in range(N_CAND):
  sigma=SIGMAS[j//REPS]; rep=j%REPS; rng=np.random.default_rng(CAND_SEED0+j); d=tr.copy(); d['context_support_distance']=d.context_support_distance.to_numpy(float)+rng.normal(0.0,sigma*scale,size=len(d)); model=fit(d,y0); s=seed_geometry(te,clean,model,coverage); mj=float(s.exclusion_jaccard.mean()); sw=int(s.membership_switches.sum())
  diagnostics.append({'candidate_index':j,'sigma':sigma,'replicate':rep,'rng_seed':CAND_SEED0+j,'mean_exclusion_jaccard':mj,'total_membership_switches':sw,'abs_mean_jaccard_difference':abs(mj-hist_j),'abs_total_switch_difference':abs(sw-hist_sw)}); models.append(model)
 diag=pd.DataFrame(diagnostics).sort_values(['abs_mean_jaccard_difference','abs_total_switch_difference','candidate_index'],kind='stable').reset_index(drop=True); chosen=int(diag.iloc[0].candidate_index); sd=diag.iloc[0].to_dict(); control=models[chosen]; cseed=seed_geometry(te,clean,control,coverage)
 seed=pseed.merge(cseed,on='generation_seed',suffixes=('_poison','_control'),validate='one_to_one'); seed['S_poison_minus_control']=seed.D_near_minus_far_poison-seed.D_near_minus_far_control
 jd=float(sd['abs_mean_jaccard_difference']); swd=float(sd['abs_total_switch_difference']); gate=bool(jd<=0.010 and swd<=0.10*hist_sw); primary=float(seed.S_poison_minus_control.mean()); pci=boot_mean(seed.S_poison_minus_control,PRIMARY_BOOT_SEED); cmean=float(seed.D_near_minus_far_control.mean()); cci=boot_mean(seed.D_near_minus_far_control,SECONDARY_BOOT_SEED)
 if not gate: decision='inconclusive_inadequate_perturbation_match'
 elif pci[0]>0: decision='poisoning_specific_localization_supported'
 elif pci[1]<=0: decision='evidence_against_poisoning_specificity'
 else: decision='specificity_unresolved'
 summary={'status':'post_review_stronger_label_preserving_control','protocol':'research/audit/experiment_166_stronger_label_preserving_control_plan.md','historical_snapshot':'d1e3285707ed788a39c7e883c157a8a359cde7db','historical_experiment_preserved':True,'candidate_count':N_CAND,'selected_candidate_index':chosen,'selected_sigma':float(sd['sigma']),'selected_replicate':int(sd['replicate']),'selected_rng_seed':int(sd['rng_seed']),'training_context_distance_sd':scale,'historical_poison_count':poison_n,'source_exclusion_coverage':coverage,'historical_poison_mean_exclusion_jaccard':hist_j,'control_mean_exclusion_jaccard':float(cseed.exclusion_jaccard.mean()),'abs_mean_jaccard_difference':jd,'historical_poison_total_membership_switches':hist_sw,'control_total_membership_switches':int(cseed.membership_switches.sum()),'abs_total_switch_difference':swd,'match_adequacy_pass':gate,'poison_mean_seed_D_near_minus_far':float(seed.D_near_minus_far_poison.mean()),'control_mean_seed_D_near_minus_far':cmean,'control_D_seed_bootstrap_ci_p025':float(cci[0]),'control_D_seed_bootstrap_ci_p975':float(cci[1]),'primary_mean_paired_S_poison_minus_control':primary,'primary_seed_bootstrap_ci_p025':float(pci[0]),'primary_seed_bootstrap_ci_p975':float(pci[1]),'primary_bootstrap_resamples':BOOT,'primary_decision':decision,'poison_fraction_switches_near_cutoff':float(seed.near_switches_poison.sum()/max(1,seed.membership_switches_poison.sum())),'control_fraction_switches_near_cutoff':float(seed.near_switches_control.sum()/max(1,seed.membership_switches_control.sum())),'poison_total_selected_action_changes':int(seed.selected_action_changes_poison.sum()),'control_total_selected_action_changes':int(seed.selected_action_changes_control.sum()),'poison_mean_abs_score_shift':float(seed.mean_abs_score_shift_poison.mean()),'control_mean_abs_score_shift':float(seed.mean_abs_score_shift_control.mean())}
 OUTDIR.mkdir(parents=True,exist_ok=True); pd.DataFrame(diagnostics).to_csv(OUTDIR/'candidate_matching_diagnostics.csv',index=False); seed.to_csv(OUTDIR/'paired_seed_results.csv',index=False); pd.DataFrame([summary]).to_csv(OUTDIR/'summary.csv',index=False); (OUTDIR/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__': main()
