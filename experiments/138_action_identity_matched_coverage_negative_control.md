# Experiment 138 — action-identity matched-coverage negative control

## Purpose

Test whether Experiment 137's context ranking adds information beyond the
trivial rule “alert every action-1 candidate.” The negative control alerted all
action-1 rows and randomly selected action-2/3 rows until matching the primary
39.02% alert budget. Five thousand random allocations were evaluated.

## Results

| Policy | Recall | Precision | Balanced accuracy | Harmful rows captured |
|---|---:|---:|---:|---:|
| Context-ranked fixed coverage | **0.815** | **0.316** | **0.750** | **1,082** |
| Action 1 only (33.3% coverage) | 0.764 | 0.347 | 0.754 | 1,014 |
| Matched random, mean | 0.784 | 0.304 | 0.732 | 1,040.8 |

Against matched random allocation, context ranking added:

- +0.0310 unsafe recall;
- +0.0120 unsafe precision;
- +0.0183 balanced accuracy;
- 41.2 additional harmful rows captured on average.

None of 5,000 random trials equaled or exceeded the primary rule on these
metrics.

## Interpretation

Most discrimination comes from action identity, but context ranking provides
real incremental value when allocating the remaining alert budget among
action-2 and action-3 candidates. The action-1-only policy has marginally higher
balanced accuracy because it abstains on fewer safe rows, but it sacrifices 5.1
percentage points of unsafe recall and misses 68 additional harmful actions.

This negative control was formulated after seeing the seventh population.
Experiments 139–140 prospectively test whether context ranking again exceeds
matched random allocation on an eighth untouched population.
