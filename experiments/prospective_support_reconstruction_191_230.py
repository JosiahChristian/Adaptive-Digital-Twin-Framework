from pathlib import Path
import experiments.action_conditioned_support_representation_analysis as source

TARGET_SEEDS=list(range(44191,44231)); RESULTS_DIR=Path("results")
source.ANALYSIS_SEEDS=TARGET_SEEDS
source.OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_191_230.csv"
source.FOLD_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_folds_191_230.csv"
source.ACTION_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_actions_191_230.csv"
source.COEFFICIENT_OUTPUT_PATH=RESULTS_DIR/"prospective_action_conditioned_support_representation_coefficients_191_230.csv"

def main():
    print("EXPERIMENT 130 - FROZEN FIFTH-POPULATION RECONSTRUCTION")
    print(f"seeds={TARGET_SEEDS[0]}-{TARGET_SEEDS[-1]} count={len(TARGET_SEEDS)}")
    print("Experiment 131 source-prior calibration protocol frozen before outcomes.")
    source.main()

if __name__=="__main__": main()
