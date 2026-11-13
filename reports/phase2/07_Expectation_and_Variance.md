## 07_Expectation and Variance of Weekday Sleep Duration

## Empirical distribution

Let X be usual weekday/workday sleep duration for a uniformly selected adult from the **4,702 exact-hour records** described in [Task 2.6](06_Continuous_Variable_and_Normal_Model.md). Each observed person receives probability `1/4702` in this unweighted empirical distribution. Values coded as *less than 3 hours* or *14 hours or more* are excluded because their exact hours are unknown.

| Quantity | Definition for the empirical distribution | Result |
|---|---|---:|
| E[X], empirical mean | Sum of the 4,702 exact durations / 4,702 | **7.7084 hours** |
| Var(X), empirical variance | Mean of `(duration - 7.7084)²` over the 4,702 records | **2.1130 hours²** |
| SD(X) | Square root of empirical variance | **1.4536 hours** |
| Median and interquartile range | Median; Q3 - Q1 | **8.0 hours; 1.5 hours** |

The expectation of **7.71 hours** is the average weekday duration in this empirical distribution. The variance measures average squared distance from that mean; its squared-hour units make it less directly readable than the standard deviation of **1.45 hours**. The median and IQR supplement the mean and variance because the recorded durations are heaped at half hours and the distribution is not exactly normal.

These calculations use denominator `n`, rather than `n - 1`, because they describe the **observed empirical distribution**. They are not an estimate of the design-based population variance or the sampling variance of a survey estimate. The mean and variance are sensitive to how grouped endpoints are handled, so the exclusion rule must accompany the result.

## Reproducibility

Run `python src/phase2_extended_analysis.py` from the project root. The calculations and sample counts are written to `data/processed/phase2/weekday_sleep_distribution_summary.csv`.
