# Phase 2.3. Conditional Probabilities

## Question

Among adults in the probability analysis set, how common is weekday sleep under 7 hours among participants who reported any supplement use, and how common is it among participants who reported no supplement use?

Let:
- A = reported any supplement use in the past 30 days.
- Aᶜ = reported no supplement use.
- B = usual weekday/workday sleep under 7 hours.

The calculation uses the same 4,741 adults defined in [Task 1](01_Events_and_Random_Variable.md). These are unweighted empirical probabilities.

## Calculations

The conditional probability formula is:

P(B | A) = P(A ∩ B) / P(A)

For supplement users, 546 of the 3,070 participants with A also belonged to B:

P(B | A) = 546 / 3,070 = 0.1779 = **17.79%**

For participants reporting no supplement use, 419 of the 1,671 participants with Aᶜ belonged to B:

P(B | Aᶜ) = 419 / 1,671 = 0.2507 = **25.07%**

| Supplement-use group | Participants in group | Under 7 hours | Conditional probability |
|---|---:|---:|---:|
| Any supplement use (A) | 3,070 | 546 | 17.79% |
| No supplement use (Aᶜ) | 1,671 | 419 | 25.07% |

The observed difference is 17.79% − 25.07% = **−7.29 percentage points** (rounded from unrounded values). In this analyzed sample, the proportion classified as usually sleeping under 7 hours is descriptively lower among participants reporting supplement use.

## Why the denominator changes

A conditional probability restricts attention to the group named after the vertical bar. For P(B | A), the denominator is the 3,070 supplement users, not all 4,741 adults. For P(B | Aᶜ), it is the 1,671 non-users. The numerators count the people in each restricted group who also meet B. This is why these conditional percentages answer a different question from the joint percentages in Task 2, which used all 4,741 adults as their denominator.

## Interpretation and limits

These are descriptive probabilities for the complete-observation sample. The difference does not establish that supplement use affects sleep: the data are cross-sectional, supplement use combines many products, and groups may differ in age or other characteristics. No significance test or causal interpretation is made here. Sampling-weighted versions and subgroup conditional probabilities are addressed in the NHANES-specific Path A requirements.

## Reproducibility

Run `python src/phase2_analysis.py` from the project root using the project environment. The script calculates these probabilities from the source XPT files and writes `conditional_probabilities.csv` under `data/processed/phase2/`. Raw XPT files are not modified.

## Data documentation

- [NHANES sleep questionnaire documentation (`SLQ_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm)
- [NHANES total supplement-use documentation (`DSQTOT_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm)
