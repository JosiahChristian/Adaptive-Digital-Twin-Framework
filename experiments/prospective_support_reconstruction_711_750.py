from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44711, 44751))
RESULTS_DIR = Path("results")
source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_711_750.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_711_750.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_711_750.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_711_750.csv"

def main():
    print("EXPERIMENT 162 - FROZEN INTERVENTION-ALIGNED METRIC TARGET RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    source.main()

if __name__ == "__main__":
    main()
