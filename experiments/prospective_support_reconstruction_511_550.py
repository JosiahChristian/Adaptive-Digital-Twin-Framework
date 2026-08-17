from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44511, 44551))
RESULTS_DIR = Path("results")
source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_511_550.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_511_550.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_511_550.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_511_550.csv"


def main():
    print("EXPERIMENT 149 - FROZEN THIRTEENTH-POPULATION RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Experiment 150 label-poisoning stress-test attack, controls, endpoints, doses, and criteria were frozen before outcomes.")
    source.main()


if __name__ == "__main__":
    main()
