## 05-Discrete Count and the Binomial Model

## Count and sampling experiment

Let **Y** be the number of adults who usually sleep under 7 hours on weekdays among **10 distinct supplement users** selected uniformly from the 3,070 supplement users in the [Phase 2 analysis set](01_Events_and_Random_Variable.md). Each selected person contributes one of two outcomes: short weekday sleep (`SLD012 < 7`) or not. Thus Y is a discrete count with possible values 0, 1, …, 10. In the fixed analyzed sample, 546 of the 3,070 supplement users meet the short-sleep definition, giving an empirical success fraction of **p = 546 / 3,070 = 0.17785**.

This is a clearly defined *resampling illustration* using the analyzed sample. It is separate from the count of 546 short sleepers observed among all 3,070 supplement users in NHANES.

## When a binomial model applies

A binomial model for Y needs a fixed number of trials, two outcomes per trial, independent trials, and the same success probability on every trial. If the 10 users were drawn **with replacement** from the fixed group, each draw would have probability p of selecting a short sleeper and the draws would be independent. Conditional on that fixed group, the count would follow `Binomial(10, 546/3070)` exactly.

Our defined experiment selects **distinct people without replacement**. Its draws are therefore dependent: after a short sleeper is selected, both the number of short sleepers and the total number of people left decrease. The exact distribution is hypergeometric, with 3,070 people, 546 short sleepers, and 10 draws. A binomial distribution with `n = 10` and `p = 546/3070` is a close approximation here because 10 / 3,070 is only **0.33%** of the group.

For example, for exactly two short sleepers:

| Model | Calculation | P(Y = 2) |
|---|---|---:|
| Binomial approximation | `C(10, 2) × p² × (1 − p)⁸` | 0.297118 (29.71%) |
| Exact sampling without replacement | `C(546, 2) × C(2524, 8) / C(3070, 10)` | 0.297634 (29.76%) |

The two probabilities differ by about **0.05 percentage point**. The script calculates the complete probability distribution for all counts from 0 through 10; this example shows how closely the two models agree for one outcome. The binomial approximation is based on the observed empirical fraction p, not a known population probability.

## Why the NHANES count is a different problem

The actual 546 short sleepers among the 3,070 analyzed supplement users should **not** be treated as the outcome of 3,070 independent, equal-probability Bernoulli trials. NHANES uses a stratified, multistage sample with unequal selection probabilities and clustering. Respondents also vary in characteristics related to sleep, and inclusion in this complete-observation subset depends on having valid supplement and sleep responses. Those features undermine the independent, common-p assumptions for a simple binomial model of the survey count. Applying a simple binomial standard error to that count would ignore the survey design.

This section is a probability-model illustration. It makes no significance test, population estimate, or causal claim about supplement use and sleep.

## Reproducibility

Run `python src/phase2_analysis.py` from the project root using the project environment. The script rebuilds the analysis set from the original XPT files and writes `data/processed/phase2/binomial_illustration.csv`, with the binomial approximation and exact without-replacement probability for each count from 0 through 10. The original files remain unchanged.
