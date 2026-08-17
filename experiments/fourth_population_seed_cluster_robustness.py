"""Experiment 128: seed-cluster robustness and calibration of Experiment 127.

The Experiment 127 models and fourth-population predictions are reconstructed
without refitting on the target. Inference resamples whole generation seeds to
respect within-seed dependence.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN=Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST=Path("results/prospective_action_conditioned_support_representation_actions_151_190.csv")
SUMMARY=Path("results/fourth_population_seed_cluster_robustness.csv")
SEEDS=Path("results/fourth_population_seed_level_performance.csv")
CAL=Path("results/fourth_population_calibration.csv")
BOOT=Path("results/fourth_population_seed_cluster_bootstrap.csv")
N_BOOT=5000
RNG_SEED=12844190
MODELS={
 "primary_action_plus_context_support":["action_2","action_3","context_support_distance"],
 "comparator_action_identity_only":["action_2","action_3"],
}


def prep(path):
    d=pd.read_csv(path)
    d["action_2"]=(d["action"].astype(int)==2).astype(int)
    d["action_3"]=(d["action"].astype(int)==3).astype(int)
    d["unsafe_action"]=d["unsafe_action"].astype(int)
    return d.dropna(subset=["generation_seed","unsafe_action","context_support_distance"]).copy()


def ece(y,p,bins=10):
    edges=np.linspace(0,1,bins+1); idx=np.clip(np.digitize(p,edges[1:-1]),0,bins-1)
    return float(sum((idx==b).mean()*abs(y[idx==b].mean()-p[idx==b].mean()) for b in range(bins) if np.any(idx==b)))


def main():
    tr,te=prep(TRAIN),prep(TEST); yt=tr.unsafe_action.to_numpy(); y=te.unsafe_action.to_numpy()
    predictions={}
    for name,features in MODELS.items():
        m=make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=5000,random_state=RNG_SEED))
        m.fit(tr[features],yt); predictions[name]=m.predict_proba(te[features])[:,1]

    summary=[]; cal=[]; seed_rows=[]
    for name,p in predictions.items():
        summary.append({"model":name,"rows":len(te),"seeds":te.generation_seed.nunique(),"roc_auc":roc_auc_score(y,p),
          "balanced_accuracy_at_0_5":balanced_accuracy_score(y,p>=.5),"brier_score":brier_score_loss(y,p),
          "log_loss":log_loss(y,p),"ece_10_bin":ece(y,p)})
        frac_pos,mean_pred=calibration_curve(y,p,n_bins=10,strategy="quantile")
        for i,(mp,fp) in enumerate(zip(mean_pred,frac_pos),1):
            cal.append({"model":name,"quantile_bin":i,"mean_predicted_probability":mp,"observed_unsafe_fraction":fp})
        for seed,g in te.assign(probability=p).groupby("generation_seed"):
            gy=g.unsafe_action.to_numpy(); gp=g.probability.to_numpy()
            seed_rows.append({"model":name,"generation_seed":int(seed),"rows":len(g),"unsafe_rows":int(gy.sum()),
              "unsafe_prevalence":gy.mean(),"roc_auc":roc_auc_score(gy,gp) if len(np.unique(gy))==2 else np.nan,
              "brier_score":brier_score_loss(gy,gp)})

    seed_values=np.sort(te.generation_seed.unique()); rng=np.random.default_rng(RNG_SEED)
    boot=[]
    primary=predictions["primary_action_plus_context_support"]; comp=predictions["comparator_action_identity_only"]
    for i in range(N_BOOT):
        selected=rng.choice(seed_values,len(seed_values),replace=True)
        idx=np.concatenate([np.flatnonzero(te.generation_seed.to_numpy()==s) for s in selected])
        by=y[idx]; pa=roc_auc_score(by,primary[idx]); ca=roc_auc_score(by,comp[idx])
        boot.append({"bootstrap":i+1,"primary_auc":pa,"action_only_auc":ca,"difference":pa-ca})
    bd=pd.DataFrame(boot)
    summary.extend([
      {"model":"cluster_bootstrap_primary","rows":len(te),"seeds":len(seed_values),"roc_auc":bd.primary_auc.mean(),
       "balanced_accuracy_at_0_5":np.percentile(bd.primary_auc,2.5),"brier_score":np.percentile(bd.primary_auc,97.5),
       "log_loss":np.nan,"ece_10_bin":np.nan},
      {"model":"cluster_bootstrap_primary_minus_action_only","rows":len(te),"seeds":len(seed_values),"roc_auc":bd.difference.mean(),
       "balanced_accuracy_at_0_5":np.percentile(bd.difference,2.5),"brier_score":np.percentile(bd.difference,97.5),
       "log_loss":(bd.difference>0).mean(),"ece_10_bin":np.nan},
    ])
    SUMMARY.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(summary).to_csv(SUMMARY,index=False); pd.DataFrame(seed_rows).to_csv(SEEDS,index=False)
    pd.DataFrame(cal).to_csv(CAL,index=False); bd.to_csv(BOOT,index=False)
    print(pd.DataFrame(summary).to_string(index=False))
    sd=pd.DataFrame(seed_rows)
    print(sd.groupby("model").roc_auc.agg(["mean","std","min","max","count"]).to_string())


if __name__=="__main__": main()
