from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44591, 44631))
RESULTS_DIR = Path("results")
source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_591_630.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_591_630.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_591_630.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_591_630.csv"


def main():
    print("EXPERIMENT 155 - FRESH FIFTEENTH-POPULATION RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Clean-vs-poison intervention endpoints and replication rule were frozen before outcomes.")
    source.main()


if __name__ == "__main__":
    main()
