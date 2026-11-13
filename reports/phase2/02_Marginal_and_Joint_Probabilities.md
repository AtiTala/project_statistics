## 02-Marginal and Joint Empirical Probabilities

## Analysis set

This calculation uses the 4,741 adults defined in [Task 1](01_Events_and_Random_Variable.md): linked NHANES records, age 20 years or older, a valid yes/no response for `DSD010`, and a non-missing response for weekday sleep (`SLD012`). These are **unweighted empirical sample probabilities**. The sampling-weighted comparison is reserved for the NHANES-specific Path A requirement.

The two events are:

- `A`: any dietary supplement use in the past 30 days (`DSD010 = 1`); `Aᶜ`: no use (`DSD010 = 2`).
- `B`: usual weekday/workday sleep under 7 hours (`SLD012 < 7`, including the grouped `<3` code).

## Marginal probabilities

For an event E, the empirical probability is its observed frequency divided by the number of eligible observations, `n = 4,741`.

| Event | Count | Empirical probability | Percent |
|---|---:|---:|---:|
| `A`: any supplement use | 3,070 | 3,070 / 4,741 = 0.6475 | 64.75% |
| `Aᶜ`: no supplement use | 1,671 | 1,671 / 4,741 = 0.3525 | 35.25% |
| `B`: weekday sleep under 7 hours | 965 | 965 / 4,741 = 0.2035 | 20.35% |
| `Bᶜ`: weekday sleep 7 hours or more | 3,776 | 3,776 / 4,741 = 0.7965 | 79.65% |

## Joint probabilities

|  | `B`: under 7 hours | `Bᶜ`: 7 hours or more | Row total |
|---|---:|---:|---:|
| `A`: any supplement use | 546 (11.52%) | 2,524 (53.24%) | 3,070 (64.75%) |
| `Aᶜ`: no supplement use | 419 (8.84%) | 1,252 (26.41%) | 1,671 (35.25%) |
| Column total | 965 (20.35%) | 3,776 (79.65%) | 4,741 (100.00%) |

For example, `P(A ∩ B) = 546 / 4,741 = 0.1152`. Each joint-cell percentage uses the full analysis-set denominator. The four joint probabilities sum to 1 before rounding, and their row and column totals agree with the marginal probabilities above. Displayed percentages may differ from 100% by 0.01 percentage point because of rounding.

## Interpretation

In this complete-observation adult sample, about 64.75% reported any supplement use, and about 20.35% were classified as usually sleeping under 7 hours on weekdays. About 11.52% of the sample met both event definitions. These are sample descriptions; they are not yet population estimates and do not show that supplement use changes sleep. NHANES weighting and conditional probabilities are handled in the following tasks.

## Reproducibility

Run `python src/phase2_analysis.py` from the project root. The script reads the original `DEMO_L.xpt`, `SLQ_L.xpt`, and `DSQTOT_L.xpt` files, checks that `SEQN` is unique within each participant-level file, recreates the adult analysis set, and writes the marginal and joint tables to `data/processed/phase2/`. The original XPT files remain unchanged.

## Data documentation

- [NHANES sleep questionnaire documentation (`SLQ_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm)
- [NHANES total supplement-use documentation (`DSQTOT_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm)
