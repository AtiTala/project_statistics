## A1_Conditional Short-Sleep Probabilities in Subgroups

## Definition

The binary outcome is usual weekday/workday sleep under 7 hours (`B`, derived from `SLD012`). Within each pre-specified age band and NHANES sex category, compare `P(B | A, subgroup)` with `P(B | Aᶜ, subgroup)`, where `A` means reported any dietary supplement use in the past 30 days. The analysis uses the **4,741-adult** [Phase 2 sample](01_Events_and_Random_Variable.md), with one person per row. These are unweighted, descriptive sample proportions.

## Age-band comparisons

| Age band | Supplement use | Adults | Short-sleep adults | Conditional probability |
|---|---|---:|---:|---:|
| 20-39 | Yes | 522 | 92 | 17.62% |
| 20-39 | No | 588 | 135 | 22.96% |
| 40-59 | Yes | 807 | 165 | 20.45% |
| 40-59 | No | 512 | 142 | 27.73% |
| 60+ | Yes | 1,741 | 289 | 16.60% |
| 60+ | No | 571 | 142 | 24.87% |

The sample short-sleep fraction is lower among supplement users in each age band. For example, among adults aged 40-59, it is 20.45% for users and 27.73% for non-users, a descriptive difference of **-7.29 percentage points**. These within-band percentages address a more focused question than the overall comparison, because the age composition of the two supplement groups differs.

## NHANES sex-category comparisons

| `RIAGENDR` category | Supplement use | Adults | Short-sleep adults | Conditional probability |
|---|---|---:|---:|---:|
| Male (code 1) | Yes | 1,203 | 232 | 19.29% |
| Male (code 1) | No | 881 | 237 | 26.90% |
| Female (code 2) | Yes | 1,867 | 314 | 16.82% |
| Female (code 2) | No | 790 | 182 | 23.04% |

The same descriptive direction appears in both released sex categories. These comparisons are **not** tests of a supplement effect: the data are observational, supplement use is broad, other characteristics may differ, and survey weights are not used in this table. No hypothesis test is performed in Phase 2.

## Reproducibility

Run `python src/phase2_extended_analysis.py` from the project root. The full subgroup counts and proportions are saved in `data/processed/phase2/path_a1_subgroup_conditional_probabilities.csv`. Age bands were defined in [Task 2.1](01_Events_and_Random_Variable.md); `RIAGENDR` codes come from the [NHANES demographics documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm).
