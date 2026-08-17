from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44551, 44591))
RESULTS_DIR = Path("results")
source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_551_590.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_551_590.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_551_590.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_551_590.csv"


def main():
    print("EXPERIMENT 152 - FROZEN FOURTEENTH-POPULATION RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Constrained-audit attack, budget, controls, endpoints, and criteria were frozen before outcomes.")
    source.main()


if __name__ == "__main__":
    main()
