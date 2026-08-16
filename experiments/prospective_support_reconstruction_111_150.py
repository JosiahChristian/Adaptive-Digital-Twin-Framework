from pathlib import Path

import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44111, 44151))
RESULTS_DIR = Path("results")

source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / (
    "prospective_action_conditioned_support_representation_111_150.csv"
)
source.FOLD_OUTPUT_PATH = RESULTS_DIR / (
    "prospective_action_conditioned_support_representation_folds_111_150.csv"
)
source.ACTION_OUTPUT_PATH = RESULTS_DIR / (
    "prospective_action_conditioned_support_representation_actions_111_150.csv"
)
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / (
    "prospective_action_conditioned_support_representation_coefficients_111_150.csv"
)


def main():
    print("=" * 180)
    print("EXPERIMENT 122 - FROZEN THIRD-POPULATION SUPPORT RECONSTRUCTION")
    print("=" * 180)
    print(f"source implementation={source.__name__}")
    print(f"prospective seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]}")
    print(f"seed count={len(TARGET_SEEDS)}")
    print("No Experiment 118-121 harm model is fit or retuned.")
    print()

    source.main()

    print()
    print("THIRD-POPULATION RECONSTRUCTION COMPLETE")
    print(f"summary={source.OUTPUT_PATH}")
    print(f"folds={source.FOLD_OUTPUT_PATH}")
    print(f"actions={source.ACTION_OUTPUT_PATH}")
    print(f"coefficients={source.COEFFICIENT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
