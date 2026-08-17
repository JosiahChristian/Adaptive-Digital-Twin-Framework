"""Experiment 150: preregistered source-training label-poisoning stress test.

Frozen before seeds 44511-44550 are generated. This defensive experiment tests
whether targeted concealment of high-context-distance unsafe source rows degrades
the prospectively replicated hazard-filter intervention more than matched random
unsafe-to-safe label contamination.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_511_550.csv")
OUT = Path("results/preregistered_training_label_poisoning_stress_test.csv")
TRIALS = Path("results/preregistered_training_label_poisoning_random_trials.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
DOSES = [0.05, 0.10, 0.20]
PRIMARY_DOSE = 0.20
N_RANDOM = 200
SOURCE_UNSAFE_RECALL_TARGET = 0.80
RNG_SEED = 15044550


def prep(path):
    d = pd.read_csv(path).copy()
    d["action_2"] = (d.action.astype(int) == 2).astype(int)
    d["action_3"] = (d.action.astype(int) == 3).astype(int)
    d["unsafe_action"] = d.unsafe_action.astype(int)
    needed = FEATURES + [
        "unsafe_action", "realized_action_regret", "predicted_action_loss",
        "generation_seed", "test_index", "action"
    ]
    return d.dropna(subset=needed).copy()


def fit_model(d, labels):
    m = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED),
    )
    m.fit(d[FEATURES], np.asarray(labels, dtype=int))
    return m


def top_n_flags(scores, n):
    flags = np.zeros(len(scores), dtype=np.int8)
    if n > 0:
        order = np.argsort(-scores, kind="stable")
        flags[order[:n]] = 1
    return flags


def choose_index(losses, actions, excluded):
    available = np.flatnonzero(excluded == 0)
    if len(available) == 0:
        available = np.arange(len(losses))
    return int(min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i]))))


def evaluate(model, te, exclusion_count):
    scores = model.predict_proba(te[FEATURES])[:, 1]
    flags = top_n_flags(scores, exclusion_count)
    tmp = te.assign(hazard_flag=flags)
    unsafe_selected = 0
    total_regret = 0.0
    changed = 0
    contexts = 0
    for _, g in tmp.groupby(["generation_seed", "test_index"], sort=True):
        if len(g) != 3:
            raise ValueError("Expected exactly three candidate actions per context")
        actions = g.action.to_numpy(dtype=int)
        losses = g.predicted_action_loss.to_numpy(dtype=float)
        regrets = g.realized_action_regret.to_numpy(dtype=float)
        unsafe = g.unsafe_action.to_numpy(dtype=int)
        ex = g.hazard_flag.to_numpy(dtype=np.int8)
        baseline_idx = choose_index(losses, actions, np.zeros(3, dtype=np.int8))
        selected_idx = choose_index(losses, actions, ex)
        unsafe_selected += int(unsafe[selected_idx])
        total_regret += float(regrets[selected_idx])
        changed += int(actions[selected_idx] != actions[baseline_idx])
        contexts += 1
    return {
        "unsafe_selected": unsafe_selected,
        "unsafe_rate": unsafe_selected / contexts,
        "total_regret": total_regret,
        "mean_regret": total_regret / contexts,
        "changed_actions": changed,
        "changed_fraction": changed / contexts,
        "contexts": contexts,
    }


def main():
    tr = prep(TRAIN).reset_index(drop=True)
    te = prep(TEST).sort_values(["generation_seed", "test_index", "action"], kind="stable").reset_index(drop=True)
    clean_labels = tr.unsafe_action.to_numpy(dtype=int)
    unsafe_idx = np.flatnonzero(clean_labels == 1)

    clean_model = fit_model(tr, clean_labels)
    source_scores = clean_model.predict_proba(tr[FEATURES])[:, 1]
    source_unsafe_scores = np.sort(source_scores[clean_labels == 1])
    source_threshold = float(source_unsafe_scores[max(0, int(np.floor((1 - SOURCE_UNSAFE_RECALL_TARGET) * len(source_unsafe_scores))))])
    frozen_coverage = float(np.mean(source_scores >= source_threshold))
    target_exclusion_count = int(round(frozen_coverage * len(te)))
    clean_metrics = evaluate(clean_model, te, target_exclusion_count)

    rng = np.random.default_rng(RNG_SEED)
    summary_rows = []
    trial_rows = []

    # Targeted order is fixed from source features and true source labels only.
    targeted_order = unsafe_idx[np.argsort(-tr.loc[unsafe_idx, "context_support_distance"].to_numpy(), kind="stable")]

    for dose in DOSES:
        flip_n = max(1, int(round(dose * len(unsafe_idx))))
        targeted_flip = targeted_order[:flip_n]
        targeted_labels = clean_labels.copy()
        targeted_labels[targeted_flip] = 0
        targeted_model = fit_model(tr, targeted_labels)
        targeted_metrics = evaluate(targeted_model, te, target_exclusion_count)

        random_unsafe = np.empty(N_RANDOM, dtype=int)
        random_regret = np.empty(N_RANDOM, dtype=float)
        for trial in range(N_RANDOM):
            flip = rng.choice(unsafe_idx, size=flip_n, replace=False)
            labels = clean_labels.copy()
            labels[flip] = 0
            m = fit_model(tr, labels)
            met = evaluate(m, te, target_exclusion_count)
            random_unsafe[trial] = met["unsafe_selected"]
            random_regret[trial] = met["total_regret"]
            trial_rows.append({
                "dose": dose,
                "trial": trial + 1,
                "flipped_source_unsafe_rows": flip_n,
                "unsafe_selected": met["unsafe_selected"],
                "total_regret": met["total_regret"],
            })

        row = {
            "dose": dose,
            "source_unsafe_rows": len(unsafe_idx),
            "flipped_source_unsafe_rows": flip_n,
            "frozen_source_coverage": frozen_coverage,
            "target_candidate_rows": len(te),
            "target_contexts": clean_metrics["contexts"],
            "target_exclusion_count": target_exclusion_count,
            "clean_unsafe_selected": clean_metrics["unsafe_selected"],
            "clean_unsafe_rate": clean_metrics["unsafe_rate"],
            "clean_total_regret": clean_metrics["total_regret"],
            "clean_mean_regret": clean_metrics["mean_regret"],
            "targeted_unsafe_selected": targeted_metrics["unsafe_selected"],
            "targeted_unsafe_rate": targeted_metrics["unsafe_rate"],
            "targeted_total_regret": targeted_metrics["total_regret"],
            "targeted_mean_regret": targeted_metrics["mean_regret"],
            "delta_targeted_unsafe_minus_clean": targeted_metrics["unsafe_selected"] - clean_metrics["unsafe_selected"],
            "delta_targeted_regret_minus_clean": targeted_metrics["total_regret"] - clean_metrics["total_regret"],
            "random_unsafe_mean": float(random_unsafe.mean()),
            "random_unsafe_p95": float(np.percentile(random_unsafe, 95)),
            "random_regret_mean": float(random_regret.mean()),
            "random_regret_p95": float(np.percentile(random_regret, 95)),
            "probability_random_unsafe_ge_targeted": float(np.mean(random_unsafe >= targeted_metrics["unsafe_selected"])),
            "probability_random_regret_ge_targeted": float(np.mean(random_regret >= targeted_metrics["total_regret"])),
        }
        if dose == PRIMARY_DOSE:
            row["criterion_targeted_unsafe_worse_than_clean"] = int(targeted_metrics["unsafe_selected"] > clean_metrics["unsafe_selected"])
            row["criterion_targeted_regret_worse_than_clean"] = int(targeted_metrics["total_regret"] > clean_metrics["total_regret"])
            row["criterion_targeted_unsafe_above_random_p95"] = int(targeted_metrics["unsafe_selected"] > row["random_unsafe_p95"])
            row["criterion_targeted_regret_above_random_p95"] = int(targeted_metrics["total_regret"] > row["random_regret_p95"])
            row["primary_vulnerability_criteria_pass"] = int(
                row["criterion_targeted_unsafe_worse_than_clean"]
                and row["criterion_targeted_regret_worse_than_clean"]
                and row["criterion_targeted_unsafe_above_random_p95"]
                and row["criterion_targeted_regret_above_random_p95"]
            )
        summary_rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(OUT, index=False)
    pd.DataFrame(trial_rows).to_csv(TRIALS, index=False)
    print(pd.DataFrame(summary_rows).to_string(index=False))


if __name__ == "__main__":
    main()
