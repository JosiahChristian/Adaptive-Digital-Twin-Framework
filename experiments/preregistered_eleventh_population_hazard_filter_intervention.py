"""Experiment 146: preregistered eleventh-population hazard-filter intervention.

Frozen before seeds 44431-44470 are generated. Evaluates whether the previously
validated source-trained action+context hazard ranking can improve simulated
candidate-action selection relative to predicted-loss baseline and matched
per-context random exclusions.
"""
from pathlib import Path
import itertools
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

TRAIN = Path("results/action_conditioned_support_representation_analysis_actions_071_110.csv")
TEST = Path("results/prospective_action_conditioned_support_representation_actions_431_470.csv")
OUT = Path("results/preregistered_eleventh_population_hazard_filter_intervention.csv")
TRIALS = Path("results/preregistered_eleventh_population_hazard_filter_random_trials.csv")
BY_SEED = Path("results/preregistered_eleventh_population_hazard_filter_by_seed.csv")
FEATURES = ["action_2", "action_3", "context_support_distance"]
SOURCE_UNSAFE_RECALL_TARGET = 0.80
REGRET_THRESHOLD = 0.005
N_RANDOM = 5000
RNG_SEED = 14644470


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


def source_model(tr):
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=5000, random_state=RNG_SEED),
    )
    model.fit(tr[FEATURES], tr.unsafe_action.to_numpy())
    return model


def top_n_flags(scores, n):
    flags = np.zeros(len(scores), dtype=np.int8)
    if n <= 0:
        return flags
    order = np.argsort(-scores, kind="stable")
    flags[order[:n]] = 1
    return flags


def choose_index(losses, actions, excluded):
    available = np.flatnonzero(excluded == 0)
    if len(available) == 0:
        available = np.arange(len(losses))
    # Stable deterministic tie break: predicted loss, then action identity.
    best = min(available.tolist(), key=lambda i: (float(losses[i]), int(actions[i])))
    return int(best)


def main():
    tr, te = prep(TRAIN), prep(TEST)
    model = source_model(tr)
    ytr = tr.unsafe_action.to_numpy()
    source_scores = model.predict_proba(tr[FEATURES])[:, 1]
    source_unsafe_scores = np.sort(source_scores[ytr == 1])
    source_threshold = float(source_unsafe_scores[max(0, int(np.floor((1 - SOURCE_UNSAFE_RECALL_TARGET) * len(source_unsafe_scores))))])
    frozen_coverage = float(np.mean(source_scores >= source_threshold))

    te = te.sort_values(["generation_seed", "test_index", "action"], kind="stable").reset_index(drop=True)
    target_scores = model.predict_proba(te[FEATURES])[:, 1]
    target_alert_n = int(round(frozen_coverage * len(te)))
    flags = top_n_flags(target_scores, target_alert_n)
    te["hazard_flag"] = flags

    contexts = []
    baseline_unsafe = 0
    primary_unsafe = 0
    baseline_regret = 0.0
    primary_regret = 0.0
    changed = 0
    seed_records = {}

    # For k exclusions among 3 candidates, enumerate all position masks once.
    masks_by_k = {
        k: [np.array(mask, dtype=np.int8) for mask in itertools.product([0, 1], repeat=3) if sum(mask) == k]
        for k in range(4)
    }

    for (seed, test_index), g in te.groupby(["generation_seed", "test_index"], sort=True):
        if len(g) != 3:
            raise ValueError(f"Expected exactly 3 actions for context {(seed, test_index)}, found {len(g)}")
        actions = g.action.to_numpy(dtype=int)
        losses = g.predicted_action_loss.to_numpy(dtype=float)
        regrets = g.realized_action_regret.to_numpy(dtype=float)
        unsafe = g.unsafe_action.to_numpy(dtype=int)
        actual_flags = g.hazard_flag.to_numpy(dtype=np.int8)

        baseline_idx = choose_index(losses, actions, np.zeros(3, dtype=np.int8))
        primary_idx = choose_index(losses, actions, actual_flags)
        k = int(actual_flags.sum())

        baseline_unsafe += int(unsafe[baseline_idx])
        primary_unsafe += int(unsafe[primary_idx])
        baseline_regret += float(regrets[baseline_idx])
        primary_regret += float(regrets[primary_idx])
        changed += int(actions[baseline_idx] != actions[primary_idx])

        rec = seed_records.setdefault(int(seed), {
            "seed": int(seed), "contexts": 0, "baseline_unsafe": 0, "primary_unsafe": 0,
            "baseline_regret": 0.0, "primary_regret": 0.0, "changed_actions": 0,
        })
        rec["contexts"] += 1
        rec["baseline_unsafe"] += int(unsafe[baseline_idx])
        rec["primary_unsafe"] += int(unsafe[primary_idx])
        rec["baseline_regret"] += float(regrets[baseline_idx])
        rec["primary_regret"] += float(regrets[primary_idx])
        rec["changed_actions"] += int(actions[baseline_idx] != actions[primary_idx])

        # Precompute the outcome selected by every matched mask for this context.
        mask_outcomes = []
        for mask in masks_by_k[k]:
            idx = choose_index(losses, actions, mask)
            mask_outcomes.append((int(unsafe[idx]), float(regrets[idx])))
        contexts.append((k, mask_outcomes))

    context_count = len(contexts)
    rng = np.random.default_rng(RNG_SEED)
    random_unsafe = np.zeros(N_RANDOM, dtype=int)
    random_regret = np.zeros(N_RANDOM, dtype=float)

    for k, outcomes in contexts:
        options = len(outcomes)
        draws = rng.integers(0, options, size=N_RANDOM)
        unsafe_options = np.asarray([o[0] for o in outcomes], dtype=int)
        regret_options = np.asarray([o[1] for o in outcomes], dtype=float)
        random_unsafe += unsafe_options[draws]
        random_regret += regret_options[draws]

    unsafe_p1 = float(np.percentile(random_unsafe, 1))
    regret_p1 = float(np.percentile(random_regret, 1))
    p_random_unsafe_as_good = float(np.mean(random_unsafe <= primary_unsafe))
    p_random_regret_as_good = float(np.mean(random_regret <= primary_regret))

    by_seed = pd.DataFrame(list(seed_records.values())).sort_values("seed")
    by_seed["delta_unsafe_primary_minus_baseline"] = by_seed.primary_unsafe - by_seed.baseline_unsafe
    by_seed["delta_regret_primary_minus_baseline"] = by_seed.primary_regret - by_seed.baseline_regret

    out = {
        "target_candidate_rows": len(te),
        "target_contexts": context_count,
        "frozen_source_coverage": frozen_coverage,
        "target_excluded_candidates": target_alert_n,
        "baseline_unsafe_selected": baseline_unsafe,
        "primary_unsafe_selected": primary_unsafe,
        "baseline_unsafe_rate": baseline_unsafe / context_count,
        "primary_unsafe_rate": primary_unsafe / context_count,
        "delta_unsafe_primary_minus_baseline": primary_unsafe - baseline_unsafe,
        "baseline_total_regret": baseline_regret,
        "primary_total_regret": primary_regret,
        "baseline_mean_regret": baseline_regret / context_count,
        "primary_mean_regret": primary_regret / context_count,
        "delta_total_regret_primary_minus_baseline": primary_regret - baseline_regret,
        "changed_selected_actions": changed,
        "changed_selected_action_fraction": changed / context_count,
        "random_unsafe_mean": float(random_unsafe.mean()),
        "random_unsafe_p1": unsafe_p1,
        "random_unsafe_p99": float(np.percentile(random_unsafe, 99)),
        "random_regret_mean": float(random_regret.mean()),
        "random_regret_p1": regret_p1,
        "random_regret_p99": float(np.percentile(random_regret, 99)),
        "probability_random_unsafe_as_good_or_better": p_random_unsafe_as_good,
        "probability_random_regret_as_good_or_better": p_random_regret_as_good,
        "criterion_unsafe_below_random_p1": int(primary_unsafe < unsafe_p1),
        "criterion_regret_below_random_p1": int(primary_regret < regret_p1),
    }
    out["all_primary_criteria_pass"] = int(
        out["criterion_unsafe_below_random_p1"] and out["criterion_regret_below_random_p1"]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([out]).to_csv(OUT, index=False)
    pd.DataFrame({
        "trial": np.arange(1, N_RANDOM + 1),
        "unsafe_selected": random_unsafe,
        "total_regret": random_regret,
    }).to_csv(TRIALS, index=False)
    by_seed.to_csv(BY_SEED, index=False)
    print(pd.DataFrame([out]).to_string(index=False))


if __name__ == "__main__":
    main()
