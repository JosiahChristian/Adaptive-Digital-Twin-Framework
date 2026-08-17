"""Audit-only adjudication of Experiment 166 from committed artifacts.

No retraining, target regeneration, preregistration change, or replacement of the
historical Experiment 166 result occurs here. Implements the three analyses frozen
in research/experiment_166_audit_adjudication_plan.md.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROWS=Path('results/preregistered_cutoff_geometry_mechanism_rows.csv')
TARGET=Path('results/prospective_action_conditioned_support_representation_actions_791_830.csv')
CHANGED=Path('results/preregistered_cutoff_geometry_context_changes.csv')
PRIMARY=Path('results/preregistered_cutoff_geometry_mechanism.csv')
OUT=Path('audit_outputs')
BOOT=10_000; PERM=10_000; RNG_SEED=16644830

def rho(a,b):
    r=spearmanr(a,b,nan_policy='omit').statistic
    return 0.0 if np.isnan(r) else float(r)

def analysis_a(rows,rng):
    rec=[]
    for seed,g in rows.groupby('generation_seed',sort=True):
        near=g.near_cutoff_primary.to_numpy(bool); sw=g.membership_switch.to_numpy(bool)
        nn=int(near.sum()); fn=int((~near).sum())
        ns=int((near&sw).sum()); fs=int(((~near)&sw).sum())
        nr=ns/nn; fr=fs/fn
        rec.append(dict(generation_seed=int(seed),near_rows=nn,far_rows=fn,near_switches=ns,far_switches=fs,near_switch_rate=nr,far_switch_rate=fr,rate_difference=nr-fr))
    ps=pd.DataFrame(rec); d=ps.rate_difference.to_numpy(float); n=len(ps)
    boots=np.array([np.mean(d[rng.choice(n,n,replace=True)]) for _ in range(BOOT)])
    x=rows.assign(near_switch=(rows.membership_switch.astype(bool)&rows.near_cutoff_primary.astype(bool)).astype(int),far_switch=(rows.membership_switch.astype(bool)&~rows.near_cutoff_primary.astype(bool)).astype(int),has_near=rows.near_cutoff_primary.astype(int),has_far=(~rows.near_cutoff_primary.astype(bool)).astype(int))
    ctx=x.groupby(['generation_seed','test_index'],as_index=False).agg(near_switch=('near_switch','max'),far_switch=('far_switch','max'),has_near=('has_near','max'),has_far=('has_far','max'))
    both=ctx[(ctx.has_near==1)&(ctx.has_far==1)]
    return ps,dict(analysis='A_context_seed_respecting_criterion1',inferential_unit='generation_seed',seeds=n,mean_seed_near_switch_rate=float(ps.near_switch_rate.mean()),mean_seed_far_switch_rate=float(ps.far_switch_rate.mean()),mean_seed_rate_difference=float(d.mean()),seed_bootstrap_difference_ci_p025=float(np.percentile(boots,2.5)),seed_bootstrap_difference_ci_p975=float(np.percentile(boots,97.5)),fraction_seeds_positive_difference=float(np.mean(d>0)),contexts_with_both_near_and_far_candidates=int(len(both)),context_level_near_switch_presence_rate=float(both.near_switch.mean()) if len(both) else None,context_level_far_switch_presence_rate=float(both.far_switch.mean()) if len(both) else None,interpretation_rule='A positive seed-bootstrap CI supports enrichment under seed-level inference; poisoning-specificity remains unresolved.')

def prepare_seed_arrays(rows,target):
    keys=['generation_seed','test_index','action']
    t=target.copy(); t[keys]=t[keys].astype(int)
    d=rows.merge(t[keys+['predicted_action_loss']],on=keys,how='left',validate='one_to_one')
    if d.predicted_action_loss.isna().any(): raise RuntimeError('predicted_action_loss merge failed')
    prepared={}
    for seed,g0 in d.groupby('generation_seed',sort=True):
        g=g0.sort_values(['test_index','action']).reset_index(drop=True)
        sizes=g.groupby('test_index').size().to_numpy()
        if not np.all(sizes==3): raise RuntimeError(f'seed {seed}: expected three candidates/context')
        nctx=len(sizes)
        prepared[int(seed)]=dict(
            unsafe=g.unsafe_action.to_numpy(int),
            clean=g.clean_excluded.to_numpy(bool),
            poison=g.poison_excluded.to_numpy(bool),
            loss=g.predicted_action_loss.to_numpy(float).reshape(nctx,3),
            unsafe2=g.unsafe_action.to_numpy(int).reshape(nctx,3),
        )
    return prepared

def unsafe_selected_count(loss,unsafe,mask):
    m=mask.reshape(loss.shape)
    available=np.where(~m,loss,np.inf)
    all_excluded=np.all(m,axis=1)
    if np.any(all_excluded): available[all_excluded]=loss[all_excluded]
    j=np.argmin(available,axis=1)
    return int(unsafe[np.arange(len(j)),j].sum())

def analysis_b(rows,target,primary,rng):
    prepared=prepare_seed_arrays(rows,target); seeds=sorted(prepared)
    observed=float(primary.iloc[0].rho_net_unsafe_crossing_delta_unsafe)
    null=np.empty(PERM,float)
    for rep in range(PERM):
        nets=np.empty(len(seeds),float); deltas=np.empty(len(seeds),float)
        for si,seed in enumerate(seeds):
            z=prepared[seed]; c=z['clean']; p=z['poison']; common=c&p
            sw=np.flatnonzero(c^p); np_only=int(np.sum(p&~c))
            if np_only*2!=len(sw): raise RuntimeError(f'seed {seed}: unequal exclusive counts')
            chosen=rng.choice(sw,size=np_only,replace=False)
            po=np.zeros(len(c),bool); po[chosen]=True
            co=np.zeros(len(c),bool); co[sw]=True; co[chosen]=False
            cn=common|co; pn=common|po; u=z['unsafe']
            nets[si]=u[po].sum()-u[co].sum()
            deltas[si]=unsafe_selected_count(z['loss'],z['unsafe2'],pn)-unsafe_selected_count(z['loss'],z['unsafe2'],cn)
        null[rep]=rho(nets,deltas)
    return null,dict(analysis='B_criterion2_bookkeeping_preserving_null',permutations=PERM,observed_spearman_rho=observed,null_mean_rho=float(null.mean()),null_median_rho=float(np.median(null)),null_ci_p025=float(np.percentile(null,2.5)),null_ci_p975=float(np.percentile(null,97.5)),one_sided_p_rho_as_or_more_negative=float((1+np.sum(null<=observed))/(PERM+1)),observed_percentile_in_null=float(np.mean(null<=observed)),null_preserves='seed/context/action candidates, unsafe labels, predicted action loss, switched set, common exclusions, fixed clean/poison exclusion counts, downstream selection rule',null_breaks='actual clean-only versus poison-only direction assignment within each seed switched set')

def analysis_c(rows,changed,rng):
    sw=rows[rows.membership_switch.astype(int)==1].copy()
    ctx=sw.assign(near_switch=sw.near_cutoff_primary.astype(int),far_switch=(~sw.near_cutoff_primary.astype(bool)).astype(int)).groupby(['generation_seed','test_index'],as_index=False).agg(near_switch=('near_switch','max'),far_switch=('far_switch','max'))
    ctx['switch_class']=np.select([(ctx.near_switch==1)&(ctx.far_switch==0),(ctx.near_switch==0)&(ctx.far_switch==1),(ctx.near_switch==1)&(ctx.far_switch==1)],['near_only','far_only','mixed'],default='invalid')
    if (ctx.switch_class=='invalid').any(): raise RuntimeError('invalid switch class')
    changed_keys=set(zip(changed.generation_seed.astype(int),changed.test_index.astype(int)))
    ctx['selected_action_changed']=[int((int(r.generation_seed),int(r.test_index)) in changed_keys) for r in ctx.itertuples(index=False)]
    grp=ctx.groupby('switch_class').selected_action_changed.agg(['count','sum','mean']).rename(columns={'sum':'changed_count','mean':'changed_rate'}).reset_index()
    rates=dict(zip(grp.switch_class,grp.changed_rate)); nr=float(rates.get('near_only',np.nan)); fr=float(rates.get('far_only',np.nan))
    seed_ids=np.array(sorted(ctx.generation_seed.unique().astype(int))); pieces={s:ctx[ctx.generation_seed==s] for s in seed_ids}
    bd=[]
    for _ in range(BOOT):
        sampled=rng.choice(seed_ids,size=len(seed_ids),replace=True)
        b=pd.concat([pieces[s] for s in sampled],ignore_index=True)
        n=b[b.switch_class=='near_only'].selected_action_changed; f=b[b.switch_class=='far_only'].selected_action_changed
        if len(n) and len(f): bd.append(float(n.mean()-f.mean()))
    bd=np.asarray(bd)
    n=ctx[ctx.switch_class=='near_only'].selected_action_changed; f=ctx[ctx.switch_class=='far_only'].selected_action_changed
    a=float(n.sum())+.5; b=float(len(n)-n.sum())+.5; c=float(f.sum())+.5; d=float(len(f)-f.sum())+.5
    return ctx,grp,dict(analysis='C_near_vs_far_downstream_specificity',switched_contexts=int(len(ctx)),near_only_contexts=int(np.sum(ctx.switch_class=='near_only')),far_only_contexts=int(np.sum(ctx.switch_class=='far_only')),mixed_contexts=int(np.sum(ctx.switch_class=='mixed')),near_only_selected_action_change_rate=nr,far_only_selected_action_change_rate=fr,near_minus_far_rate_difference=float(nr-fr),seed_bootstrap_difference_ci_p025=float(np.percentile(bd,2.5)),seed_bootstrap_difference_ci_p975=float(np.percentile(bd,97.5)),bootstrap_valid_resamples=int(len(bd)),haldane_corrected_near_vs_far_odds_ratio=float((a*d)/(b*c)),mixed_contexts_reported_separately=True)

def main():
    OUT.mkdir(exist_ok=True)
    rows=pd.read_csv(ROWS); target=pd.read_csv(TARGET); changed=pd.read_csv(CHANGED); primary=pd.read_csv(PRIMARY)
    if sorted(rows.generation_seed.unique().astype(int).tolist())!=list(range(44791,44831)): raise RuntimeError('frozen target seed mismatch')
    if not (rows.groupby(['generation_seed','test_index']).size()==3).all(): raise RuntimeError('three-candidate invariant failed')
    ps,sa=analysis_a(rows,np.random.default_rng(RNG_SEED+1))
    null,sb=analysis_b(rows,target,primary,np.random.default_rng(RNG_SEED+2))
    ctx,grp,sc=analysis_c(rows,changed,np.random.default_rng(RNG_SEED+3))
    ps.to_csv(OUT/'analysis_a_seed_level.csv',index=False)
    pd.DataFrame({'null_rho':null}).to_csv(OUT/'analysis_b_null_distribution.csv',index=False)
    ctx.to_csv(OUT/'analysis_c_switched_contexts.csv',index=False); grp.to_csv(OUT/'analysis_c_group_summary.csv',index=False)
    summary=dict(status='audit_only_existing_artifacts',source_snapshot='d1e3285707ed788a39c7e883c157a8a359cde7db',historical_experiment_result_preserved=True,new_model_fit=False,new_target_population=False,matched_clean_to_clean_control_run=False,analysis_a=sa,analysis_b=sb,analysis_c=sc)
    (OUT/'experiment_166_existing_artifact_adjudication.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__': main()
