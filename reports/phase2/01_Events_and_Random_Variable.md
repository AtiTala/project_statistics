# Phase 2.1. Events and Random Variable

## Purpose

This section translates the project question into probability notation. The target population remains adults aged 20 years or older represented by NHANES August 2021–August 2023. Each observation is one participant, identified by `SEQN`.

## Probability analysis set

For the initial empirical probability calculations, include participants who:

1. have linked records in `DEMO_L`, `SLQ_L`, and `DSQTOT_L`;
2. are aged 20 years or older (`RIDAGEYR >= 20`);
3. have a valid yes/no response for any supplement use (`DSD010` is 1 or 2); and
4. have a non-missing weekday/workday sleep response (`SLD012`).

Using the downloaded files, this initial complete-observation set contains **4,741 adults**. Each participant appears once. The unweighted empirical probabilities will use this set as their denominator. A separate weighted version will be computed using positive `WTDRD1` values and reported as a population-oriented estimate; it will not be mixed with the unweighted sample proportions.

## Events

For the unweighted empirical probability, treat each participant in the observed probability analysis set as equally likely to be selected. This describes the analyzed sample. The separate `WTDRD1`-weighted estimate is the population-oriented version and accounts for the NHANES selection weights.

- **Event A — Any supplement use:** the participant reported taking at least one dietary supplement in the past 30 days (`DSD010 = 1`). Its complement, `Aᶜ`, is a valid report of no supplement use (`DSD010 = 2`). Refused, “don’t know,” and missing responses are outside this analysis set rather than being coded as “no.”
- **Event B — Weekday short sleep:** the participant’s usual weekday/workday sleep duration is less than 7 hours. In `SLD012`, code `2` means “less than 3 hours,” so it belongs to B; exact reported values from 3 through 6.5 hours also belong to B. Values of 7 hours or more, including the grouped code `14` (“14 hours or more”), are not members of B (they belong to `Bᶜ`). Missing sleep responses are excluded from the analysis set.

The 7-hour cutoff is a pre-specified project definition for a binary probability event, informed by CDC guidance that adults generally need at least 7 hours of sleep. It is not a clinical diagnosis and does not imply that all adults have the same sleep needs. NHANES records the low and high sleep endpoints as grouped categories, so code `2` is classified as below 7 hours and code `14` as not below 7 hours; neither is treated as an exact number of hours.

## Random variable

Let **X** be the participant’s usual weekday/workday sleep duration, measured in hours and recorded in `SLD012`. X is a quantitative random variable with half-hour increments for exact values. Because the released codes `2` and `14` represent ranges, analyses of X’s numeric expectation and variance must state how those grouped endpoints are handled. For the binary event B, their categories are sufficient to determine whether sleep is below 7 hours.

For subgroup comparisons, the event B will be examined across the pre-specified age bands (`20–39`, `40–59`, and `60+`) and NHANES sex categories (`RIAGENDR` 1 and 2). These comparisons are descriptive probability calculations; Phase 2 does not perform formal hypothesis tests.

## Link to the project question

The central probability comparisons will include `P(B | A)` and `P(B | Aᶜ)`: the empirical probability of weekday short sleep among supplement users and among non-users. Other quantities in the next section can include the marginal probabilities `P(A)` and `P(B)`, their joint probability `P(A ∩ B)`, and conditional probabilities within the pre-specified age or sex groups. Differences will be interpreted descriptively and will not be described as causal effects.

## Data documentation

- [NHANES sleep questionnaire documentation (`SLQ_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm)
- [NHANES total supplement-use documentation (`DSQTOT_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm)
- [NHANES demographics documentation (`DEMO_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm)
- [CDC adult sleep guidance](https://www.cdc.gov/sleep/about/)
