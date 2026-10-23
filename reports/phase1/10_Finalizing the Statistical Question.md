## 10. Finalizing the Statistical Question

### Final statistical question

Among adults aged 20 years or older represented in NHANES August 2021–August 2023, how do the distributions of usual weekday/workday sleep duration and usual weekend/non-workday sleep duration compare between participants who reported using any dietary supplement in the past 30 days and participants who reported no dietary supplement use?

### Why this question fits the available data

The question uses participant-level information that can be linked by the NHANES respondent identifier, `SEQN`. The supplement-use file, `DSQTOT_L`, identifies participants who reported any supplement use and those who reported none. The sleep questionnaire file, `SLQ_L`, provides usual sleep-duration measures for weekdays/workdays (`SLD012`) and weekends/non-workdays (`SLD013`). The demographic file, `DEMO_L`, provides age for defining the adult population.

The preliminary merge contained 6,064 adults aged 20 years or older. Among them, 4,779 had a valid yes/no response for the any-supplement-use measure. The number included in each sleep comparison will depend on whether the participant also has a valid value for that sleep outcome. The final analysis counts and the handling of NHANES sampling weights and design variables will be documented in the relevant Path A sections.

### Statistical nature and interpretation

This is a descriptive comparison and an observational association question. The participant is the unit of observation. The analysis will compare the observed sleep-duration distributions of supplement users and non-users; it will not estimate a causal effect of supplements on sleep.

In the preliminary unweighted comparison, the median sleep duration was 8 hours in both groups for both weekday/workday and weekend/non-workday sleep. This indicates that the medians alone do not show a clear difference. It does not establish that the groups are identical: the full distributions and properly weighted estimates should be examined before drawing conclusions.

### Scope and limitations

“Any dietary supplement use” combines many different products and ingredients, so the exposure is broad and does not identify which supplement, dose, or reason for use is associated with sleep duration. NHANES 2021–2023 did not collect respondents’ reasons for taking supplements; therefore, this project cannot determine whether participants used a supplement to improve sleep. In addition, the data are observational and cross-sectional, so the results will be interpreted as differences or associations, not as evidence that supplement use causes a change in sleep.

A melatonin-specific comparison may be considered as an exploratory secondary analysis. The preliminary data identified about 101 adult melatonin reporters with a valid yes/no supplement-use response, so that subgroup may be too small for precise population estimates. Any such analysis will be treated cautiously and its precision assessed using the appropriate NHANES design.

### Preliminary expectation

Before conducting the final analysis, no directional difference is assumed. The preliminary unweighted medians were the same in the two broad supplement-use groups, so the analysis will examine whether other features of the distributions differ and whether the findings change after applying the appropriate NHANES weights.