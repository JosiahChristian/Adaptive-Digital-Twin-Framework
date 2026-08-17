"""Experiment 158: preregistered prediction-decision divergence evaluation."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_631_670.csv")
OUT = Path("results/preregistered_prediction_decision_divergence.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
POISON_DOSE = 0.20
SOURCE_UNSAFE_RECALL_TARGET = 0.80
RNG_SEED = 15844670


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


def evaluate_decisions(te, mask):
    tmp = te.assign(excluded=mask)
    unsafe = 0; regret = 0.0; contexts = 0
    for _, g in tmp.groupby(["generation_seed", "test_index"], sort=True):
        losses = g.predicted_action_loss.to_numpy(float)
        actions = g.action.to_numpy(int)
        excluded = g.excluded.to_numpy(bool)
        available = np.flatnonzero(~excluded)
        if len(available) == 0:
            available = np.arange(len(g))
        idx = int(min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))
        unsafe += int(g.unsafe_action.to_numpy(int)[idx])
        regret += float(g.realized_action_regret.to_numpy(float)[idx])
        contexts += 1
    return unsafe, regret, contexts


def direction(clean_vals, poison_vals, lower_is_better=False):
    if lower_is_better:
        better = sum(p < c for c,p in zip(clean_vals, poison_vals))
        worse = sum(p > c for c,p in zip(clean_vals, poison_vals))
    else:
        better = sum(p > c for c,p in zip(clean_vals, poison_vals))
        worse = sum(p < c for c,p in zip(clean_vals, poison_vals))
    if better >= 2 and worse == 0:
        return "improves"
    if worse >= 2 and better == 0:
        return "degrades"
    return "mixed"


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

    y = te.unsafe_action.to_numpy(int)
    cs = clean_model.predict_proba(te[FEATURES])[:,1]
    ps = poison_model.predict_proba(te[FEATURES])[:,1]
    cm = top_n_mask(cs, exclusion_count); pm = top_n_mask(ps, exclusion_count)

    clean_auc = roc_auc_score(y, cs); poison_auc = roc_auc_score(y, ps)
    clean_ap = average_precision_score(y, cs); poison_ap = average_precision_score(y, ps)
    clean_recall = float(y[cm].sum()/max(1,y.sum())); poison_recall = float(y[pm].sum()/max(1,y.sum()))
    cu, cr, contexts = evaluate_decisions(te, cm)
    pu, pr, _ = evaluate_decisions(te, pm)

    pred_base = direction([clean_auc, clean_ap, clean_recall], [poison_auc, poison_ap, poison_recall], lower_is_better=False)
    pred_dir = "prediction_" + pred_base
    if pu < cu and pr < cr:
        dec_dir = "decision_improves"
    elif pu > cu and pr > cr:
        dec_dir = "decision_degrades"
    else:
        dec_dir = "decision_mixed"

    strong = ((pred_dir == "prediction_degrades" and dec_dir == "decision_improves") or
              (pred_dir == "prediction_improves" and dec_dir == "decision_degrades"))
    divergence = strong or ((pred_dir == "prediction_mixed") and dec_dir in {"decision_improves","decision_degrades"})

    row = {
        "target_rows": len(te), "target_contexts": contexts, "target_exclusion_count": exclusion_count,
        "clean_auc": clean_auc, "poison_auc": poison_auc,
        "clean_ap": clean_ap, "poison_ap": poison_ap,
        "clean_excluded_unsafe_recall": clean_recall, "poison_excluded_unsafe_recall": poison_recall,
        "clean_unsafe_selected": cu, "poison_unsafe_selected": pu,
        "clean_total_regret": cr, "poison_total_regret": pr,
        "prediction_direction": pred_dir, "decision_direction": dec_dir,
        "prediction_decision_divergence": int(divergence),
        "strong_divergence": int(strong),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(OUT, index=False)
    print(pd.DataFrame([row]).to_string(index=False))


if __name__ == "__main__":
    main()
