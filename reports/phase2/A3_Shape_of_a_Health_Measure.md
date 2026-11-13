## A3_Shape of a Health-Related Measurement

## Selected measure

The health-related measurement is usual **weekday/workday sleep duration**, derived from sleep and wake times in `SLD012`. The released values are rounded to half hours, and the two endpoint codes are grouped categories. For numerical shape analysis, use the **4,702 exact-hour values from 3 to 13.5 hours** within the Phase 2 adult sample. The remaining **39** endpoint-coded records are kept for the binary short-sleep event but do not enter the numerical duration summary.

The histogram and normal Q-Q display are shown in [Task 2.6](06_Continuous_Variable_and_Normal_Model.md). The mean is **7.71 hours**, median **8.0 hours**, and sample skewness **-0.18**. This indicates mild negative skew by a numeric measure, although the most striking shape feature is concentration at round and half-hour values. The distribution is unimodal around 7-8 hours and does not follow a smooth normal curve closely.

## Unusual values and normal approximation

The first and third quartiles are **7.0** and **8.5 hours**, so the IQR is **1.5 hours**. A descriptive Tukey rule places fences at **4.75** and **10.75 hours**. There are **137** exact-hour observations below the lower fence and **106** above the upper fence, for **243 flagged observations** in total. The observed exact-hour range is **3.0 to 13.5 hours**. These flags identify unusual values under this rule; they are **not automatically errors and are not deleted**. The 39 grouped endpoint codes require separate handling because their precise durations are undisclosed.

The normal curve misses the heaping and parts of both tails, as the Q-Q plot shows. It is only a rough approximation for the center and should not be assumed for the individual-level duration distribution. These are unweighted sample descriptions, not population estimates or clinical diagnoses.

## Reproducibility and source

Run `python src/phase2_extended_analysis.py` from the project root. Results are in `data/processed/phase2/weekday_sleep_distribution_summary.csv`. The [NHANES sleep documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm) explains the derived values, half-hour rounding, and endpoint categories.
