"""Experiment 166: preregistered local cutoff-geometry mechanism adjudication."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.contingency_tables import StratifiedTable

TRAIN=Path('results/action_conditioned_support_representation_analysis_actions_071_110.csv')
TEST=Path('results/prospective_action_conditioned_support_representation_actions_791_830.csv')
OUT=Path('results/preregistered_cutoff_geometry_mechanism.csv')
SEED_OUT=Path('results/preregistered_cutoff_geometry_mechanism_by_seed.csv')
ROW_OUT=Path('results/preregistered_cutoff_geometry_mechanism_rows.csv')
CTX_OUT=Path('results/preregistered_cutoff_geometry_context_changes.csv')
FEATURES=['action_2','action_3','context_support_distance']
POISON_DOSE=0.20
SOURCE_UNSAFE_RECALL_TARGET=0.80
PRIMARY_BAND=0.10
BOOT=10000
RNG_SEED=16644830
TARGET_SEEDS=list(range(44791,44831))


def prep(path):
    d=pd.read_csv(path).copy()
    d['action_2']=(d.action.astype(int)==2).astype(int)
    d['action_3']=(d.action.astype(int)==3).astype(int)
    d['unsafe_action']=d.unsafe_action.astype(int)
    return d.dropna(subset=FEATURES+['unsafe_action','realized_action_regret','predicted_action_loss','generation_seed','test_index','action']).copy()


def fit(d,y):
    m=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',max_iter=5000,random_state=RNG_SEED))
    m.fit(d[FEATURES],y)
    return m


def topn(scores,n):
    mask=np.zeros(len(scores),bool)
    mask[np.argsort(-scores,kind='stable')[:n]]=True
    return mask


def select_actions(g, excluded):
    tmp=g.assign(excluded=np.asarray(excluded,bool))
    rows=[]
    for (seed,idx),c in tmp.groupby(['generation_seed','test_index'],sort=True):
        c=c.reset_index(drop=True)
        avail=np.flatnonzero(~c.excluded.to_numpy(bool))
        if len(avail)==0:
            avail=np.arange(len(c))
        losses=c.predicted_action_loss.to_numpy(float)
        actions=c.action.to_numpy(int)
        j=min(avail.tolist(),key=lambda i:(float(losses[i]),int(actions[i])))
        rows.append({'generation_seed':int(seed),'test_index':int(idx),'action':int(actions[j]),'unsafe_action':int(c.unsafe_action.iloc[j]),'realized_action_regret':float(c.realized_action_regret.iloc[j])})
    return pd.DataFrame(rows)


def rho(a,b):
    r=spearmanr(a,b,nan_policy='omit').statistic
    return 0.0 if np.isnan(r) else float(r)


def main():
    tr=prep(TRAIN).reset_index(drop=True)
    te=prep(TEST).sort_values(['generation_seed','test_index','action']).reset_index(drop=True)
    assert sorted(te.generation_seed.unique().astype(int).tolist())==TARGET_SEEDS
    assert (te.groupby(['generation_seed','test_index']).size()==3).all()

    y0=tr.unsafe_action.to_numpy(int)
    unsafe_idx=np.flatnonzero(y0==1)
    clean_model=fit(tr,y0)
    source_scores=clean_model.predict_proba(tr[FEATURES])[:,1]
    source_unsafe=np.sort(source_scores[y0==1])
    threshold=float(source_unsafe[max(0,int(np.floor((1-SOURCE_UNSAFE_RECALL_TARGET)*len(source_unsafe))))])
    coverage=float(np.mean(source_scores>=threshold))

    poison_order=unsafe_idx[np.argsort(-tr.loc[unsafe_idx,'context_support_distance'].to_numpy(),kind='stable')]
    poison_n=max(1,int(round(POISON_DOSE*len(unsafe_idx))))
    py=y0.copy(); py[poison_order[:poison_n]]=0
    assert int(np.sum(y0!=py))==poison_n
    poison_model=fit(tr,py)

    seed_rows=[]; raw_rows=[]; changed_contexts=[]; strata=[]
    for seed,g0 in te.groupby('generation_seed',sort=True):
        g=g0.reset_index(drop=True).copy(); y=g.unsafe_action.to_numpy(int)
        k=int(round(coverage*len(g)))
        cs=clean_model.predict_proba(g[FEATURES])[:,1]
        ps=poison_model.predict_proba(g[FEATURES])[:,1]
        cm=topn(cs,k); pm=topn(ps,k)
        assert int(cm.sum())==int(pm.sum())==k
        cutoff=float(np.min(cs[cm]))
        margin=np.abs(cs-cutoff)
        band_n=max(1,int(np.ceil(PRIMARY_BAND*len(g))))
        near=np.zeros(len(g),bool); near[np.argsort(margin,kind='stable')[:band_n]]=True
        switch=cm^pm; conly=cm&~pm; ponly=pm&~cm
        assert int(switch.sum())==int(conly.sum()+ponly.sum())

        a=int(np.sum(near&switch)); b=int(np.sum(near&~switch)); c=int(np.sum(~near&switch)); d=int(np.sum(~near&~switch))
        strata.append(np.array([[a,b],[c,d]],dtype=float))

        for i,row in g.iterrows():
            raw_rows.append({'generation_seed':int(seed),'test_index':int(row.test_index),'action':int(row.action),'unsafe_action':int(row.unsafe_action),'realized_action_regret':float(row.realized_action_regret),'clean_score':float(cs[i]),'poison_score':float(ps[i]),'delta_score':float(ps[i]-cs[i]),'clean_excluded':int(cm[i]),'poison_excluded':int(pm[i]),'membership_switch':int(switch[i]),'clean_cutoff_score':cutoff,'abs_clean_cutoff_margin':float(margin[i]),'near_cutoff_primary':int(near[i])})

        csel=select_actions(g,cm); psel=select_actions(g,pm)
        merged=csel.merge(psel,on=['generation_seed','test_index'],suffixes=('_clean','_poison'))
        changed=merged[merged.action_clean!=merged.action_poison].copy()
        for _,r in changed.iterrows():
            changed_contexts.append({'generation_seed':int(seed),'test_index':int(r.test_index),'clean_action':int(r.action_clean),'poison_action':int(r.action_poison),'clean_unsafe':int(r.unsafe_action_clean),'poison_unsafe':int(r.unsafe_action_poison),'transition':('unsafe' if r.unsafe_action_clean else 'safe')+'-to-'+('unsafe' if r.unsafe_action_poison else 'safe'),'clean_regret':float(r.realized_action_regret_clean),'poison_regret':float(r.realized_action_regret_poison),'delta_regret':float(r.realized_action_regret_poison-r.realized_action_regret_clean)})
        trans=pd.Series([x['transition'] for x in changed_contexts if x['generation_seed']==int(seed)]).value_counts()
        cu=int(csel.unsafe_action.sum()); pu=int(psel.unsafe_action.sum()); cr=float(csel.realized_action_regret.sum()); pr=float(psel.realized_action_regret.sum())
        inter=int(np.sum(cm&pm)); union=int(np.sum(cm|pm))
        seed_rows.append({'generation_seed':int(seed),'target_rows':len(g),'target_contexts':int(g.test_index.nunique()),'exclusion_count':k,'clean_cutoff_score':cutoff,'membership_switches':int(switch.sum()),'near_cutoff_rows':int(near.sum()),'near_cutoff_switches':a,'far_cutoff_switches':c,'clean_only_exclusions':int(conly.sum()),'poison_only_exclusions':int(ponly.sum()),'unsafe_clean_only_exclusions':int(y[conly].sum()),'unsafe_poison_only_exclusions':int(y[ponly].sum()),'net_unsafe_crossing':int(y[ponly].sum()-y[conly].sum()),'clean_unsafe_selected':cu,'poison_unsafe_selected':pu,'delta_unsafe_selected':pu-cu,'clean_total_regret':cr,'poison_total_regret':pr,'delta_regret':pr-cr,'exclusion_jaccard':inter/union if union else 1.0,'unsafe_to_safe':int(trans.get('unsafe-to-safe',0)),'safe_to_unsafe':int(trans.get('safe-to-unsafe',0)),'safe_to_safe':int(trans.get('safe-to-safe',0)),'unsafe_to_unsafe':int(trans.get('unsafe-to-unsafe',0)),'delta_auc':float(roc_auc_score(y,ps)-roc_auc_score(y,cs)),'delta_ap':float(average_precision_score(y,ps)-average_precision_score(y,cs)),'delta_recall':float(y[pm].sum()/max(1,y.sum())-y[cm].sum()/max(1,y.sum()))})

    s=pd.DataFrame(seed_rows)
    tables=np.stack(strata,axis=2)
    st=StratifiedTable(tables,shift_zeros=True)
    mh_or=float(st.oddsratio_pooled); ci=st.oddsratio_pooled_confint(alpha=0.05); cmh=st.test_null_odds(correction=False)
    r=rho(s.net_unsafe_crossing,s.delta_unsafe_selected)
    rng=np.random.default_rng(RNG_SEED); idx=np.arange(len(s)); boots=[]
    for _ in range(BOOT):
        b=rng.choice(idx,size=len(idx),replace=True); sb=s.iloc[b]; boots.append(rho(sb.net_unsafe_crossing,sb.delta_unsafe_selected))
    rci=np.percentile(boots,[2.5,97.5])
    c1=int(mh_or>1 and ci[0]>1 and float(cmh.pvalue)<0.05); c2=int(r<0 and rci[1]<0)
    summary={'seeds':len(s),'poison_count':poison_n,'source_exclusion_coverage':coverage,'primary_near_cutoff_fraction':PRIMARY_BAND,'mh_common_odds_ratio':mh_or,'mh_ci_p025':float(ci[0]),'mh_ci_p975':float(ci[1]),'cmh_two_sided_p':float(cmh.pvalue),'criterion1_cutoff_localization_pass':c1,'rho_net_unsafe_crossing_delta_unsafe':r,'boot_rho_p025':float(rci[0]),'boot_rho_p975':float(rci[1]),'criterion2_composition_direction_pass':c2,'primary_cutoff_geometry_mechanism_support':int(c1 and c2),'total_membership_switches':int(s.membership_switches.sum()),'fraction_switches_near_cutoff':float(s.near_cutoff_switches.sum()/max(1,s.membership_switches.sum())),'mean_exclusion_jaccard':float(s.exclusion_jaccard.mean()),'total_unsafe_to_safe':int(s.unsafe_to_safe.sum()),'total_safe_to_unsafe':int(s.safe_to_unsafe.sum()),'rho_net_unsafe_crossing_delta_regret':rho(s.net_unsafe_crossing,s.delta_regret),'mean_delta_auc':float(s.delta_auc.mean()),'mean_delta_ap':float(s.delta_ap.mean()),'mean_delta_recall':float(s.delta_recall.mean())}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame([summary]).to_csv(OUT,index=False); s.to_csv(SEED_OUT,index=False); pd.DataFrame(raw_rows).to_csv(ROW_OUT,index=False); pd.DataFrame(changed_contexts).to_csv(CTX_OUT,index=False)
    print('EXPERIMENT 166 - PREREGISTERED CUTOFF-GEOMETRY ADJUDICATION')
    print('Zero-cell convention: statsmodels StratifiedTable(shift_zeros=True); all 40 frozen strata retained.')
    print(pd.DataFrame([summary]).to_string(index=False))

if __name__=='__main__': main()
