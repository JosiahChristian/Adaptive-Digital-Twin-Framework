"""Audit-only adjudication of Experiment 166 using committed artifacts.

This script does NOT retrain models, regenerate target populations, modify the
preregistered experiment, or replace its historical result. It executes the
three existing-artifact analyses frozen in
research/experiment_166_audit_adjudication_plan.md:

A. context/seed-respecting robustness for Criterion 1;
B. bookkeeping-preserving permutation null for Criterion 2;
C. near-only versus far-only downstream specificity.

All outputs are audit/robustness results distinct from Experiment 166 itself.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROWS = Path("results/preregistered_cutoff_geometry_mechanism_rows.csv")
TARGET = Path("results/prospective_action_conditioned_support_representation_actions_791_830.csv")
CHANGED = Path("results/preregistered_cutoff_geometry_context_changes.csv")
PRIMARY = Path("results/preregistered_cutoff_geometry_mechanism.csv")
OUTDIR = Path("audit_outputs")

BOOT = 10_000
PERM = 10_000
RNG_SEED = 16644830


def select_actions(g: pd.DataFrame, excluded: np.ndarray) -> pd.DataFrame:
    tmp = g.assign(excluded=np.asarray(excluded, dtype=bool))
    rows = []
    for (seed, idx), c in tmp.groupby(["generation_seed", "test_index"], sort=True):
        c = c.reset_index(drop=True)
        avail = np.flatnonzero(~c.excluded.to_numpy(bool))
        if len(avail) == 0:
            avail = np.arange(len(c))
        losses = c.predicted_action_loss.to_numpy(float)
        actions = c.action.to_numpy(int)
        j = min(avail.tolist(), key=lambda i: (float(losses[i]), int(actions[i])))
        rows.append(
            {
                "generation_seed": int(seed),
                "test_index": int(idx),
                "action": int(actions[j]),
                "unsafe_action": int(c.unsafe_action.iloc[j]),
            }
        )
    return pd.DataFrame(rows)


def safe_rho(a: np.ndarray, b: np.ndarray) -> float:
    r = spearmanr(a, b, nan_policy="omit").statistic
    return 0.0 if np.isnan(r) else float(r)


def analysis_a(rows: pd.DataFrame, rng: np.random.Generator) -> dict:
    # Seed is the independent inferential unit. Candidate rows contribute only
    # to descriptive within-seed rates; uncertainty is obtained by resampling
    # entire seeds, so no Bernoulli independence of candidate rows is assumed.
    per_seed = []
    for seed, g in rows.groupby("generation_seed", sort=True):
        near = g.near_cutoff_primary.to_numpy(bool)
        sw = g.membership_switch.to_numpy(bool)
        near_n = int(near.sum())
        far_n = int((~near).sum())
        near_sw = int((near & sw).sum())
        far_sw = int(((~near) & sw).sum())
        nr = near_sw / near_n if near_n else np.nan
        fr = far_sw / far_n if far_n else np.nan
        per_seed.append(
            {
                "generation_seed": int(seed),
                "near_rows": near_n,
                "far_rows": far_n,
                "near_switches": near_sw,
                "far_switches": far_sw,
                "near_switch_rate": nr,
                "far_switch_rate": fr,
                "rate_difference": nr - fr,
                "rate_ratio": nr / fr if fr > 0 else np.inf if nr > 0 else np.nan,
            }
        )
    ps = pd.DataFrame(per_seed)
    diffs = ps.rate_difference.to_numpy(float)
    seeds = np.arange(len(ps))
    boots = np.empty(BOOT, dtype=float)
    for i in range(BOOT):
        b = rng.choice(seeds, size=len(seeds), replace=True)
        boots[i] = float(np.mean(diffs[b]))

    # Context-level descriptive aggregation: each context contributes one row
    # here, preventing the three candidates from being counted as three
    # independent inferential observations. The response is whether that
    # context has >=1 near/far switch.
    ctx = (
        rows.assign(
            near_switch=(rows.membership_switch.astype(bool) & rows.near_cutoff_primary.astype(bool)).astype(int),
            far_switch=(rows.membership_switch.astype(bool) & ~rows.near_cutoff_primary.astype(bool)).astype(int),
            has_near=rows.near_cutoff_primary.astype(int),
            has_far=(~rows.near_cutoff_primary.astype(bool)).astype(int),
        )
        .groupby(["generation_seed", "test_index"], as_index=False)
        .agg(
            near_switch=("near_switch", "max"),
            far_switch=("far_switch", "max"),
            has_near=("has_near", "max"),
            has_far=("has_far", "max"),
        )
    )
    # Only contexts containing both near and far candidates permit a within-
    # context comparison. This is secondary/descriptive because conditioning
    # on this subset changes the estimand.
    both = ctx[(ctx.has_near == 1) & (ctx.has_far == 1)].copy()
    context_near_rate = float(both.near_switch.mean()) if len(both) else np.nan
    context_far_rate = float(both.far_switch.mean()) if len(both) else np.nan

    return {
        "per_seed": ps,
        "summary": {
            "analysis": "A_context_seed_respecting_criterion1",
            "inferential_unit": "generation_seed",
            "seeds": int(len(ps)),
            "mean_seed_near_switch_rate": float(ps.near_switch_rate.mean()),
            "mean_seed_far_switch_rate": float(ps.far_switch_rate.mean()),
            "mean_seed_rate_difference": float(ps.rate_difference.mean()),
            "seed_bootstrap_difference_ci_p025": float(np.percentile(boots, 2.5)),
            "seed_bootstrap_difference_ci_p975": float(np.percentile(boots, 97.5)),
            "fraction_seeds_positive_difference": float(np.mean(diffs > 0)),
            "contexts_with_both_near_and_far_candidates": int(len(both)),
            "context_level_near_switch_presence_rate": context_near_rate,
            "context_level_far_switch_presence_rate": context_far_rate,
            "interpretation_rule": (
                "Positive seed-bootstrap CI supports robustness of enrichment to seed-level inference; "
                "it does not establish poisoning-specificity."
            ),
        },
    }


def analysis_b(rows: pd.DataFrame, target: pd.DataFrame, primary: pd.DataFrame, rng: np.random.Generator) -> dict:
    target = target.copy()
    target["generation_seed"] = target.generation_seed.astype(int)
    target["test_index"] = target.test_index.astype(int)
    target["action"] = target.action.astype(int)
    merge_cols = ["generation_seed", "test_index", "action"]
    dat = rows.merge(
        target[merge_cols + ["predicted_action_loss"]], on=merge_cols, how="left", validate="one_to_one"
    )
    if dat.predicted_action_loss.isna().any():
        raise RuntimeError("Missing predicted_action_loss after target merge")

    observed = float(primary.iloc[0].rho_net_unsafe_crossing_delta_unsafe)
    seed_groups = {int(seed): g.reset_index(drop=True) for seed, g in dat.groupby("generation_seed", sort=True)}
    seed_ids = sorted(seed_groups)

    null_rho = np.empty(PERM, dtype=float)
    for rep in range(PERM):
        net = []
        delta = []
        for seed in seed_ids:
            g = seed_groups[seed]
            clean = g.clean_excluded.to_numpy(bool)
            poison = g.poison_excluded.to_numpy(bool)
            common = clean & poison
            switch_idx = np.flatnonzero(clean ^ poison)
            poison_only_n = int(np.sum(poison & ~clean))
            if poison_only_n * 2 != len(switch_idx):
                raise RuntimeError(f"Seed {seed}: unequal exclusive-set counts")

            chosen = rng.choice(switch_idx, size=poison_only_n, replace=False)
            ponly = np.zeros(len(g), dtype=bool)
            ponly[chosen] = True
            conly = np.zeros(len(g), dtype=bool)
            conly[switch_idx] = True
            conly[chosen] = False
            clean_null = common | conly
            poison_null = common | ponly

            unsafe = g.unsafe_action.to_numpy(int)
            net.append(int(unsafe[ponly].sum() - unsafe[conly].sum()))
            csel = select_actions(g, clean_null)
            psel = select_actions(g, poison_null)
            delta.append(int(psel.unsafe_action.sum() - csel.unsafe_action.sum()))
        null_rho[rep] = safe_rho(np.asarray(net), np.asarray(delta))

    lower_p = float((1 + np.sum(null_rho <= observed)) / (PERM + 1))
    return {
        "null_rho": null_rho,
        "summary": {
            "analysis": "B_criterion2_bookkeeping_preserving_null",
            "permutations": PERM,
            "observed_spearman_rho": observed,
            "null_mean_rho": float(np.mean(null_rho)),
            "null_median_rho": float(np.median(null_rho)),
            "null_ci_p025": float(np.percentile(null_rho, 2.5)),
            "null_ci_p975": float(np.percentile(null_rho, 97.5)),
            "one_sided_p_rho_as_or_more_negative": lower_p,
            "observed_percentile_in_null": float(np.mean(null_rho <= observed)),
            "null_preserves": (
                "seed/context/action candidates, unsafe labels, predicted action loss, switch set, "
                "common exclusions, fixed clean/poison exclusion counts, and downstream selection rule"
            ),
            "null_breaks": "actual clean-only versus poison-only direction assignment within each seed's switched set",
        },
    }


def analysis_c(rows: pd.DataFrame, changed: pd.DataFrame, rng: np.random.Generator) -> dict:
    sw = rows[rows.membership_switch.astype(int) == 1].copy()
    ctx = (
        sw.assign(
            near_switch=sw.near_cutoff_primary.astype(int),
            far_switch=(~sw.near_cutoff_primary.astype(bool)).astype(int),
        )
        .groupby(["generation_seed", "test_index"], as_index=False)
        .agg(near_switch=("near_switch", "max"), far_switch=("far_switch", "max"))
    )
    ctx["switch_class"] = np.select(
        [
            (ctx.near_switch == 1) & (ctx.far_switch == 0),
            (ctx.near_switch == 0) & (ctx.far_switch == 1),
            (ctx.near_switch == 1) & (ctx.far_switch == 1),
        ],
        ["near_only", "far_only", "mixed"],
        default="invalid",
    )
    if (ctx.switch_class == "invalid").any():
        raise RuntimeError("Invalid switched-context classification")

    changed_keys = set(
        zip(changed.generation_seed.astype(int).tolist(), changed.test_index.astype(int).tolist())
    )
    ctx["selected_action_changed"] = [
        int((int(r.generation_seed), int(r.test_index)) in changed_keys) for r in ctx.itertuples(index=False)
    ]

    grouped = (
        ctx.groupby("switch_class")
        .selected_action_changed.agg(["count", "sum", "mean"])
        .rename(columns={"sum": "changed_count", "mean": "changed_rate"})
        .reset_index()
    )
    rates = dict(zip(grouped.switch_class, grouped.changed_rate))
    nrate = float(rates.get("near_only", np.nan))
    frate = float(rates.get("far_only", np.nan))
    observed_diff = nrate - frate

    seed_ids = np.array(sorted(ctx.generation_seed.unique().astype(int)))
    bootdiff = []
    for _ in range(BOOT):
        sampled = rng.choice(seed_ids, size=len(seed_ids), replace=True)
        pieces = []
        for draw_i, seed in enumerate(sampled):
            p = ctx[ctx.generation_seed == seed].copy()
            p["bootstrap_seed_instance"] = draw_i
            pieces.append(p)
        b = pd.concat(pieces, ignore_index=True)
        bn = b[b.switch_class == "near_only"].selected_action_changed
        bf = b[b.switch_class == "far_only"].selected_action_changed
        if len(bn) and len(bf):
            bootdiff.append(float(bn.mean() - bf.mean()))
    bootdiff = np.asarray(bootdiff, dtype=float)

    # Haldane-Anscombe corrected descriptive odds ratio to remain finite if a
    # cell is zero; inference is based on the seed bootstrap rate difference.
    near = ctx[ctx.switch_class == "near_only"].selected_action_changed
    far = ctx[ctx.switch_class == "far_only"].selected_action_changed
    a = float(near.sum()) + 0.5
    b = float(len(near) - near.sum()) + 0.5
    c = float(far.sum()) + 0.5
    d = float(len(far) - far.sum()) + 0.5
    or_corr = (a * d) / (b * c)

    return {
        "contexts": ctx,
        "grouped": grouped,
        "summary": {
            "analysis": "C_near_vs_far_downstream_specificity",
            "switched_contexts": int(len(ctx)),
            "near_only_contexts": int(np.sum(ctx.switch_class == "near_only")),
            "far_only_contexts": int(np.sum(ctx.switch_class == "far_only")),
            "mixed_contexts": int(np.sum(ctx.switch_class == "mixed")),
            "near_only_selected_action_change_rate": nrate,
            "far_only_selected_action_change_rate": frate,
            "near_minus_far_rate_difference": float(observed_diff),
            "seed_bootstrap_difference_ci_p025": float(np.percentile(bootdiff, 2.5)),
            "seed_bootstrap_difference_ci_p975": float(np.percentile(bootdiff, 97.5)),
            "bootstrap_valid_resamples": int(len(bootdiff)),
            "haldane_corrected_near_vs_far_odds_ratio": float(or_corr),
            "mixed_contexts_reported_separately": True,
        },
    }


def main() -> None:
    OUTDIR.mkdir(exist_ok=True)
    rows = pd.read_csv(ROWS)
    target = pd.read_csv(TARGET)
    changed = pd.read_csv(CHANGED)
    primary = pd.read_csv(PRIMARY)

    expected_seeds = list(range(44791, 44831))
    if sorted(rows.generation_seed.unique().astype(int).tolist()) != expected_seeds:
        raise RuntimeError("Row artifact does not contain the frozen 40 target seeds")
    if not (rows.groupby(["generation_seed", "test_index"]).size() == 3).all():
        raise RuntimeError("Expected exactly three action candidates per context")

    rng_a = np.random.default_rng(RNG_SEED + 1)
    rng_b = np.random.default_rng(RNG_SEED + 2)
    rng_c = np.random.default_rng(RNG_SEED + 3)

    a = analysis_a(rows, rng_a)
    b = analysis_b(rows, target, primary, rng_b)
    c = analysis_c(rows, changed, rng_c)

    a["per_seed"].to_csv(OUTDIR / "analysis_a_seed_level.csv", index=False)
    pd.DataFrame({"null_rho": b["null_rho"]}).to_csv(OUTDIR / "analysis_b_null_distribution.csv", index=False)
    c["contexts"].to_csv(OUTDIR / "analysis_c_switched_contexts.csv", index=False)
    c["grouped"].to_csv(OUTDIR / "analysis_c_group_summary.csv", index=False)

    summary = {
        "status": "audit_only_existing_artifacts",
        "source_snapshot": "d1e3285707ed788a39c7e883c157a8a359cde7db",
        "historical_experiment_result_preserved": True,
        "new_model_fit": False,
        "new_target_population": False,
        "matched_clean_to_clean_control_run": False,
        "analysis_a": a["summary"],
        "analysis_b": b["summary"],
        "analysis_c": c["summary"],
    }
    (OUTDIR / "experiment_166_existing_artifact_adjudication.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
