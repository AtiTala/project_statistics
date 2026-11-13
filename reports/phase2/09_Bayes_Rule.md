## 09_Bayes' Rule for Supplement Use and Short Sleep

## Updating the direction of the question

The [previous conditional calculation](03_Conditional_Probabilities.md) asked for the probability of short weekday sleep **given supplement use**, `P(B | A)`. Here the question is reversed: among adults who usually sleep under 7 hours on weekdays, what fraction reported any dietary supplement use in the past 30 days? With `A` = supplement use and `B` = short weekday sleep, this is `P(A | B)`.

In the same **4,741-adult unweighted analysis set**, `P(A) = 3,070/4,741 = 0.64754`, `P(B | A) = 546/3,070 = 0.17785`, and `P(B) = 965/4,741 = 0.20354`. Bayes' rule gives:

`P(A | B) = P(B | A) × P(A) / P(B)`

`= (546/3070) × (3070/4741) / (965/4741) = 546/965 = 0.5658`.

Thus **56.58%** of the 965 short-sleep adults reported supplement use. For comparison, `P(A | Bᶜ) = 2,524/3,776 = 66.84%`. The overall supplement-use fraction before conditioning on sleep is **64.75%**. The changed denominator explains why `P(A | B)` differs from `P(B | A) = 17.79%`.

Bayes' rule reorganizes the same observed joint and marginal frequencies; it does not add new evidence or make a causal claim. These are empirical sample probabilities, and the survey-weighted comparison is handled in [Path A4](A4_Raw_and_Weighted_Probability.md).

## Reproducibility

Run `python src/phase2_extended_analysis.py` from the project root. The calculation is written to `data/processed/phase2/bayes_reverse_conditional.csv`; the underlying counts can also be checked in [Task 2.2](02_Marginal_and_Joint_Probabilities.md).
