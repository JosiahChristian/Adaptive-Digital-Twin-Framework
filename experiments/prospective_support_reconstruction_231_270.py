from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source
TARGET_SEEDS=list(range(44231,44271)); RESULTS_DIR=Path("results")
source.ANALYSIS_SEEDS=TARGET_SEEDS
source.OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_231_270.csv"
source.FOLD_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_folds_231_270.csv"
source.ACTION_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_actions_231_270.csv"
source.COEFFICIENT_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_coefficients_231_270.csv"
def main():
    print("EXPERIMENT 133 - FROZEN SIXTH-POPULATION RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Experiment 134 unlabeled-EM calibration protocol frozen before outcomes.")
    source.main()
if __name__=="__main__": main()
