"""Experiment 148: exact prospective replication of Experiment 146 on new seeds."""
from pathlib import Path
import experiments.preregistered_eleventh_population_hazard_filter_intervention as source

source.TEST = Path("results/prospective_action_conditioned_support_representation_actions_471_510.csv")
source.OUT = Path("results/preregistered_twelfth_population_intervention_replication.csv")
source.TRIALS = Path("results/preregistered_twelfth_population_intervention_replication_random_trials.csv")
source.BY_SEED = Path("results/preregistered_twelfth_population_intervention_replication_by_seed.csv")
source.RNG_SEED = 14844510


def main():
    print("EXPERIMENT 148 - PREREGISTERED TWELFTH-POPULATION INTERVENTION REPLICATION")
    print("Policy, coverage rule, endpoints, random-control design, trial count, and criteria unchanged from Experiment 146.")
    source.main()


if __name__ == "__main__":
    main()
