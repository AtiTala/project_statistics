## 04-Independence of Events

## Question and analysis set

Are the events of reporting any dietary supplement use and usually sleeping under 7 hours on weekdays independent in the empirical distribution of the analyzed adults?

Use the same **4,741 adults** and event definitions as in [Task 1](01_Events_and_Random_Variable.md): `A` means any supplement use in the past 30 days (`DSD010 = 1`), and `B` means usual weekday/workday sleep under 7 hours (`SLD012 < 7`). The analysis includes adults age 20 or older with valid values for both variables. All probabilities below are **unweighted sample proportions**.

## Criterion for independence

Two events are independent when knowing whether one occurred leaves the probability of the other unchanged. One equivalent criterion is **P(A ∩ B) = P(A) × P(B)**. We compare the observed joint proportion with the product of the two observed marginal proportions. Exact equality is the independence condition for a probability distribution; a finite sample can depart from equality through sampling variation.

## Empirical comparison

| Quantity | Calculation | Empirical value |
|---|---:|---:|
| P(A): any supplement use | 3,070 / 4,741 | 0.6475 (64.75%) |
| P(B): weekday sleep under 7 hours | 965 / 4,741 | 0.2035 (20.35%) |
| Observed P(A ∩ B): both events | 546 / 4,741 | 0.1152 (11.52%) |
| P(A) × P(B): joint probability under independence | (3,070 / 4,741) × (965 / 4,741) | 0.1318 (13.18%) |

The observed joint proportion is **1.66 percentage points lower** than the product of the marginal proportions (`0.1152 − 0.1318 ≈ −0.0166`). The unrounded calculations are stored in `data/processed/phase2/independence_comparison.csv`.

The [conditional probabilities in Task 3](03_Conditional_Probabilities.md) give the same picture: P(B | A) = 546 / 3,070 = **17.79%**, while P(B | Aᶜ) = 419 / 1,671 = **25.07%**. If A and B were independent in this empirical distribution, these conditional proportions would equal the overall P(B) of 20.35%.

## Interpretation and limits

**The empirical distribution of this analyzed sample does not satisfy the independence equality.** Short weekday sleep is less common among respondents reporting any supplement use than among respondents reporting no supplement use. This is a descriptive sample association. Sampling variation, differences between the groups, and self-reported measurements all matter when interpreting it. A conclusion about independence in the wider population would require survey-design-aware inference, which is outside this descriptive task. The cross-sectional comparison does not show that supplements cause a change in sleep.

## Reproducibility

Run `python src/phase2_analysis.py` from the project root with the project environment active. The script reads the original XPT files, recreates the complete-observation adult sample, and writes `data/processed/phase2/independence_comparison.csv`. The [marginal and joint counts in Task 2](02_Marginal_and_Joint_Probabilities.md) provide a separate check of the calculations.
