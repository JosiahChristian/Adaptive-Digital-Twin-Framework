from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS = list(range(44671, 44711))
RESULTS_DIR = Path("results")
source.ANALYSIS_SEEDS = TARGET_SEEDS
source.OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_671_710.csv"
source.FOLD_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_folds_671_710.csv"
source.ACTION_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_actions_671_710.csv"
source.COEFFICIENT_OUTPUT_PATH = RESULTS_DIR / "prospective_action_conditioned_support_representation_coefficients_671_710.csv"


def main():
    print("EXPERIMENT 160 - FROZEN SEED-LEVEL COUPLING TARGET RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Seed-level coupling metrics, discordance criteria, and bootstrap were frozen before target outcomes.")
    source.main()


if __name__ == "__main__":
    main()
