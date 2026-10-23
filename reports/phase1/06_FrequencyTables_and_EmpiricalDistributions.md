## 6. Frequency Tables and Empirical Distributions

The following are preliminary, unweighted descriptive summaries for the 6,064 participants aged 20 years or older in the participant-level dataset created by linking `DEMO_L`, `SLQ_L`, and `DSQTOT_L` using `SEQN`. Each participant contributes at most one row to this dataset. The number of valid observations differs by variable because some responses are missing or were recorded as refused or “don’t know.” These summaries describe the current analysis dataset and are not population estimates.

### Categorical variables

| Variable | Category | Frequency (n) | Percent |
|---|---|---:|---:|
| Age group | 20–39 years | 1,559 | 25.7% |
| Age group | 40–59 years | 1,733 | 28.6% |
| Age group | 60 years or older | 2,772 | 45.7% |
| NHANES sex category | Category 1 | 2,720 | 44.9% |
| NHANES sex category | Category 2 | 3,344 | 55.1% |
| Supplement use (`DSD010`) | Yes | 3,092 | 64.7% of valid yes/no responses |
| Supplement use (`DSD010`) | No | 1,687 | 35.3% of valid yes/no responses |

The age-group and sex percentages use all 6,064 adults as the denominator. For supplement use, the percentages are calculated among the 4,779 participants with a valid “yes” or “no” response. In the full adult dataset, `DSD010` also has 10 refused responses, 4 “don’t know” responses, and 1,271 missing values. These responses are not classified as “no.”

### Empirical distributions of sleep duration

NHANES records the sleep-duration variables in hours, usually in half-hour increments. To summarize the observed distributions, values were grouped as less than 7 hours, 7–8.5 hours, or 9 hours or more. The percentages below use the number of valid responses for each sleep variable.

| Sleep duration | Less than 7 hours | 7–8.5 hours | 9 hours or more | Valid n |
|---|---:|---:|---:|---:|
| Weekdays/workdays (`SLD012`) | 1,269 (21.2%) | 3,350 (55.8%) | 1,381 (23.0%) | 6,000 |
| Weekends/non-workdays (`SLD013`) | 816 (13.6%) | 2,860 (47.7%) | 2,322 (38.7%) | 5,998 |

The largest group reported 7–8.5 hours of sleep on weekdays. Weekend reports were more spread toward longer durations: a larger share fell in the 9-hours-or-more group, and a smaller share fell below 7 hours, compared with weekday reports. This is a descriptive pattern only; it does not establish that people sleep significantly longer on weekends or explain why the pattern occurs.

NHANES codes 2 as “less than 3 hours” and 14 as “14 hours or more.” These endpoint responses were included in the broad groups above as less than 7 hours and 9 hours or more, respectively; they were not treated as exact values of 2 or 14 hours. Missing sleep responses were excluded from the denominator for each sleep variable.

Sources: NHANES documentation for [`SLQ_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm) and [`DSQTOT_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm). Counts and percentages were calculated from the project’s downloaded XPT files.