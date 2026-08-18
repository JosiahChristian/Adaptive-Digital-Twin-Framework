#!/usr/bin/env python3
"""Generate manuscript-only Experiment 166 stronger-control figures from the preserved CI artifact.

This script does not rerun Experiment 166. It requires the original GitHub Actions
artifact ZIP and refuses to proceed unless its SHA-256 matches the verified digest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt

EXPECTED_SHA256 = "ced924c850aa5f6b5dd2923bcd6e761f00a3a15bbae620c639c4084fa876c904"
OUTDIR = Path(__file__).resolve().parent / "generated"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_summary(artifact_zip: Path) -> dict:
    observed = sha256(artifact_zip)
    if observed != EXPECTED_SHA256:
        raise RuntimeError(
            "Artifact digest mismatch. Refusing to render. "
            f"Expected {EXPECTED_SHA256}, observed {observed}."
        )
    with zipfile.ZipFile(artifact_zip, "r") as zf:
        with zf.open("summary.json") as f:
            return json.load(f)


def plot_enrichment(summary: dict) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    labels = ["Poison", "Matched non-poison control"]
    values = [
        float(summary["poison_mean_seed_D_near_minus_far"]),
        float(summary["control_mean_seed_D_near_minus_far"]),
    ]

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.bar(labels, values)
    ax.set_ylabel("Mean seed near-minus-far membership-switch enrichment")
    ax.set_title("Experiment 166 cutoff-localization point estimates")
    ax.tick_params(axis="x", labelrotation=12)
    fig.tight_layout()
    path = OUTDIR / "fig1_experiment166_poison_vs_matched_control_enrichment.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_paired_contrast(summary: dict) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    estimate = float(summary["primary_mean_paired_S_poison_minus_control"])
    lower = float(summary["primary_seed_bootstrap_ci_p025"])
    upper = float(summary["primary_seed_bootstrap_ci_p975"])
    yerr = [[estimate - lower], [upper - estimate]]

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.errorbar([0], [estimate], yerr=yerr, fmt="o", capsize=5)
    ax.axhline(0.0, linewidth=1)
    ax.set_xlim(-0.75, 0.75)
    ax.set_xticks([0], ["Poison − matched control"])
    ax.set_ylabel("Paired difference in near-minus-far enrichment")
    ax.set_title("Frozen poisoning-specificity contrast")
    fig.tight_layout()
    path = OUTDIR / "fig2_experiment166_specificity_contrast.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "artifact_zip",
        type=Path,
        help="Path to the original experiment166-stronger-label-preserving-control ZIP artifact.",
    )
    args = parser.parse_args()

    summary = load_summary(args.artifact_zip)
    if summary.get("primary_decision") != "specificity_unresolved":
        raise RuntimeError("Unexpected primary decision in verified artifact.")
    if not bool(summary.get("match_adequacy_pass")):
        raise RuntimeError("Verified artifact does not report an adequate perturbation match.")

    p1 = plot_enrichment(summary)
    p2 = plot_paired_contrast(summary)
    print(f"Wrote {p1}")
    print(f"Wrote {p2}")


if __name__ == "__main__":
    main()
