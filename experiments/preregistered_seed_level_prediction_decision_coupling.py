"""Experiment 161: preregistered seed-level prediction-decision coupling test."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_671_710.csv")
OUT = Path("results/preregistered_seed_level_prediction_decision_coupling.csv")
SEED_OUT = Path("results/preregistered_seed_level_prediction_decision_coupling_by_seed.csv")
BOOT_OUT = Path("results/preregistered_seed_level_prediction_decision_coupling_bootstrap.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
POISON_DOSE = 0.20
SOURCE_UNSAFE_RECALL_TARGET = 0.80
BOOTSTRAPS = 10000
RNG_SEED = 16144710


def prep(path):
    d = pd.read_csv(path).copy()
    d["action_2"] = (d.action.astype(int) == 2).astype(int)
    d["action_3"] = (d.action.astype(int) == 3).astype(int)
    d["unsafe_action"] = d.unsafe_action.astype(int)
    needed = FEATURES + ["unsafe_action", "realized_action_regret", "predicted_action_loss", "generation_seed", "test_index", "action"]
    return d.dropna(subset=needed).copy()


def fit_model(d, labels):
    m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED))
    m.fit(d[FEATURES], np.asarray(labels, dtype=int))
    return m


def top_n_mask(scores, n):
    mask = np.zeros(len(scores), dtype=bool)
    if n > 0:
        mask[np.argsort(-scores, kind="stable")[:n]] = True
    return mask


def seed_decisions(g, mask):
    tmp = g.assign(excluded=mask)
    unsafe = 0; regret = 0.0; contexts = 0
    for _, c in tmp.groupby("test_index", sort=True):
        losses = c.predicted_action_loss.to_numpy(float)
        actions = c.action.to_numpy(int)
        excluded = c.excluded.to_numpy(bool)
        avail = np.flatnonzero(~excluded)
        if len(avail) == 0:
            avail = np.arange(len(c))
        idx = int(min(avail.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))
        unsafe += int(c.unsafe_action.to_numpy(int)[idx])
        regret += float(c.realized_action_regret.to_numpy(float)[idx])
        contexts += 1
    return unsafe, regret, contexts


def rankcorr(x, y):
    x = pd.Series(x).rank(method="average").to_numpy(float)
    y = pd.Series(y).rank(method="average").to_numpy(float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def discord_fraction(pred_delta, decision_delta):
    pred_delta = np.asarray(pred_delta, float); decision_delta = np.asarray(decision_delta, float)
    ok = np.isfinite(pred_delta) & np.isfinite(decision_delta) & (pred_delta != 0) & (decision_delta != 0)
    if not ok.any():
        return np.nan
    return float(np.mean(np.sign(pred_delta[ok]) == np.sign(decision_delta[ok])))


def metrics(df, scores, mask):
    y = df.unsafe_action.to_numpy(int)
    auc = roc_auc_score(y, scores) if len(np.unique(y)) == 2 else np.nan
    ap = average_precision_score(y, scores) if y.sum() > 0 else np.nan
    recall = float(y[mask].sum()/y.sum()) if y.sum() > 0 else np.nan
    return auc, ap, recall


def main():
    tr = prep(TRAIN).reset_index(drop=True)
    te = prep(TEST).sort_values(["generation_seed", "test_index", "action"], kind="stable").reset_index(drop=True)
    clean = tr.unsafe_action.to_numpy(int)
    unsafe_idx = np.flatnonzero(clean == 1)
    clean_model = fit_model(tr, clean)
    source_scores = clean_model.predict_proba(tr[FEATURES])[:,1]
    sorted_unsafe_scores = np.sort(source_scores[clean == 1])
    threshold = float(sorted_unsafe_scores[max(0, int(np.floor((1-SOURCE_UNSAFE_RECALL_TARGET)*len(sorted_unsafe_scores))))])
    coverage = float(np.mean(source_scores >= threshold))
    exclusion_count = int(round(coverage * len(te)))

    targeted_order = unsafe_idx[np.argsort(-tr.loc[unsafe_idx,"context_support_distance"].to_numpy(), kind="stable")]
    poison_n = max(1, int(round(POISON_DOSE*len(unsafe_idx))))
    poisoned = clean.copy(); poisoned[targeted_order[:poison_n]] = 0
    poison_model = fit_model(tr, poisoned)

    cs_all = clean_model.predict_proba(te[FEATURES])[:,1]
    ps_all = poison_model.predict_proba(te[FEATURES])[:,1]
    cm_all = top_n_mask(cs_all, exclusion_count)
    pm_all = top_n_mask(ps_all, exclusion_count)
    te = te.assign(clean_score=cs_all, poison_score=ps_all, clean_excluded=cm_all, poison_excluded=pm_all)

    rows = []
    for seed, g in te.groupby("generation_seed", sort=True):
        idx = g.index.to_numpy()
        ca, cap, cr = metrics(g, g.clean_score.to_numpy(float), g.clean_excluded.to_numpy(bool))
        pa, pap, pr = metrics(g, g.poison_score.to_numpy(float), g.poison_excluded.to_numpy(bool))
        cu, creg, contexts = seed_decisions(g, g.clean_excluded.to_numpy(bool))
        pu, preg, _ = seed_decisions(g, g.poison_excluded.to_numpy(bool))
        rows.append({
            "generation_seed": int(seed), "contexts": contexts,
            "clean_auc": ca, "poison_auc": pa, "delta_auc": pa-ca if np.isfinite(ca) and np.isfinite(pa) else np.nan,
            "clean_ap": cap, "poison_ap": pap, "delta_ap": pap-cap if np.isfinite(cap) and np.isfinite(pap) else np.nan,
            "clean_excluded_unsafe_recall": cr, "poison_excluded_unsafe_recall": pr,
            "delta_excluded_unsafe_recall": pr-cr if np.isfinite(cr) and np.isfinite(pr) else np.nan,
            "clean_unsafe_selected": cu, "poison_unsafe_selected": pu, "delta_unsafe_selected": pu-cu,
            "clean_total_regret": creg, "poison_total_regret": preg, "delta_regret": preg-creg,
        })
    sd = pd.DataFrame(rows)

    pairs = [
        ("auc_regret", "delta_auc", "delta_regret"),
        ("auc_unsafe", "delta_auc", "delta_unsafe_selected"),
        ("ap_regret", "delta_ap", "delta_regret"),
        ("recall_unsafe", "delta_excluded_unsafe_recall", "delta_unsafe_selected"),
    ]
    corrs = {}
    for name, x, y in pairs:
        z = sd[[x,y]].dropna()
        corrs[name] = rankcorr(z[x], z[y])
    disc_regret = discord_fraction(sd.delta_auc, sd.delta_regret)
    disc_unsafe = discord_fraction(sd.delta_auc, sd.delta_unsafe_selected)

    abs_corrs = [abs(v) for v in corrs.values() if np.isfinite(v)]
    criterion1 = len(abs_corrs) == 4 and max(abs_corrs) <= 0.50
    criterion2 = sum(v < 0.30 for v in abs_corrs) >= 2
    criterion3 = np.isfinite(disc_regret) and disc_regret >= 0.25
    criterion4 = np.isfinite(disc_unsafe) and disc_unsafe >= 0.25
    passed = criterion1 and criterion2 and criterion3 and criterion4

    rng = np.random.default_rng(RNG_SEED)
    boot_rows = []
    n = len(sd)
    for b in range(BOOTSTRAPS):
        samp = sd.iloc[rng.integers(0, n, n)].reset_index(drop=True)
        row = {"bootstrap": b+1}
        for name, x, y in pairs:
            z = samp[[x,y]].dropna()
            row[f"rho_{name}"] = rankcorr(z[x], z[y])
        row["discord_auc_regret"] = discord_fraction(samp.delta_auc, samp.delta_regret)
        row["discord_auc_unsafe"] = discord_fraction(samp.delta_auc, samp.delta_unsafe_selected)
        boot_rows.append(row)
    boot = pd.DataFrame(boot_rows)

    summary = {
        "seeds": len(sd), "target_rows": len(te), "target_exclusion_count": exclusion_count,
        **{f"rho_{k}":v for k,v in corrs.items()},
        "discord_auc_regret": disc_regret, "discord_auc_unsafe": disc_unsafe,
        "criterion_all_abs_rho_le_050": int(criterion1),
        "criterion_two_abs_rho_lt_030": int(criterion2),
        "criterion_auc_regret_discord_ge_025": int(criterion3),
        "criterion_auc_unsafe_discord_ge_025": int(criterion4),
        "weak_coupling_pass": int(passed),
    }
    for col in [c for c in boot.columns if c != "bootstrap"]:
        vals = boot[col].dropna().to_numpy(float)
        summary[f"{col}_boot_p025"] = float(np.percentile(vals, 2.5)) if len(vals) else np.nan
        summary[f"{col}_boot_p975"] = float(np.percentile(vals, 97.5)) if len(vals) else np.nan

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([summary]).to_csv(OUT, index=False)
    sd.to_csv(SEED_OUT, index=False)
    boot.to_csv(BOOT_OUT, index=False)
    print(pd.DataFrame([summary]).to_string(index=False))


if __name__ == "__main__":
    main()
