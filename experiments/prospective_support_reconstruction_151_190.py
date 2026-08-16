from pathlib import Path

import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44151, 44191))
RESULTS_DIR = Path("results")

source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_151_190.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_151_190.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_151_190.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_151_190.csv"


def main():
    print("=" * 180)
    print("EXPERIMENT 126 - FROZEN FOURTH-POPULATION SUPPORT RECONSTRUCTION")
    print("=" * 180)
    print(f"source implementation={source.__name__}")
    print(f"prospective seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]}")
    print(f"seed count={len(TARGET_SEEDS)}")
    print("Experiment 127 confirmatory model frozen before these outcomes exist.")
    print("Frozen model: action identity plus context support; training population 071-110.")
    print()
    source.main()
    print()
    print("FOURTH-POPULATION RECONSTRUCTION COMPLETE")
    print(f"summary={source.OUTPUT_PATH}")
    print(f"folds={source.FOLD_OUTPUT_PATH}")
    print(f"actions={source.ACTION_OUTPUT_PATH}")
    print(f"coefficients={source.COEFFICIENT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
