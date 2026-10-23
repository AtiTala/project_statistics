## 7. Measures of Center and Spread

The summaries below use the same preliminary, unweighted dataset as in Section 6: participants aged 20 years or older with records in the linked `DEMO_L`, `SLQ_L`, and `DSQTOT_L` files. The number of valid observations varies by variable. These are descriptive summaries of the current dataset, not weighted population estimates.

| Variable | Valid n | Mean* | SD* | Median | Q1 | Q3 | IQR | Observed endpoints in the released data |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Weekday/workday sleep (`SLD012`), hours | 6,000 | 7.70 | 1.59 | 8.0 | 7.0 | 8.5 | 1.5 | 2 = less than 3 hours; 14 = 14 hours or more |
| Weekend/non-workday sleep (`SLD013`), hours | 5,998 | 8.26 | 1.71 | 8.0 | 7.5 | 9.0 | 1.5 | 2 = less than 3 hours; 14 = 14 hours or more |
| Age at screening (`RIDAGEYR`), years | 6,064 | 53.85 | 17.18 | 57.0 | 39.0 | 68.0 | 29.0 | 20 to 80; 80 represents 80 years or older |

/ For the sleep variables, the mean and standard deviation were calculated using the numeric values as released by NHANES. Because the endpoint codes 2 and 14 represent grouped durations rather than exact values, these mean and SD estimates are approximate summaries of the released codes. The median and IQR are emphasized because they describe the center and middle spread without relying strongly on those extreme endpoint values.

The weekday and weekend sleep medians are both 8 hours, and both IQRs are 1.5 hours. The weekend mean based on the released codes is higher than the weekday mean, and the weekend upper quartile is 9 hours compared with 8.5 hours on weekdays. These are descriptive differences only; no inferential claim is made at this stage.

For age, the mean is slightly lower than the median, and the middle half of the sample falls between 39 and 68 years. Because NHANES top-codes ages of 80 years or older as 80, the reported maximum should be interpreted as “80 or older,” not necessarily exactly 80.

Sources: [NHANES sleep questionnaire documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm) and [NHANES demographics documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm). Statistics were calculated from the project’s downloaded XPT files.