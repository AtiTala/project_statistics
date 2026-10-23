## 4. Classification of Main Variables and Measurement Scales

The main outcome variables are usual sleep duration on weekdays and weekends. The main explanatory variable is dietary supplement use. At this preliminary stage, supplement use is defined broadly as reported use versus no reported use during the reference period. If the analysis is later narrowed to a specific supplement type or ingredient, that exposure will be defined at the participant level using the reported-product file and the NHANES product and ingredient reference files.

| Variable | NHANES variable or source | Role in the project | Variable type and measurement scale |
|---|---|---|---|

| Usual weekday sleep duration | `SLD012` in `SLQ_L` | Outcome | Quantitative numerical variable, recorded in hours in half-hour increments for most values; ratio scale |
| Usual weekend sleep duration | `SLD013` in `SLQ_L` | Outcome | Quantitative numerical variable, recorded in hours in half-hour increments for most values; ratio scale |
| Any dietary supplement use | Participant-level use information in `DSQTOT_L` | Main explanatory or grouping variable | Categorical, binary, nominal: reported use / no reported use |
| Supplement type or ingredient, if selected for a narrower analysis | Derived from `DSQIDS_L` and the `DSPI`, `DSII`, and `DSBI` reference files | More specific explanatory or grouping variable | Categorical, nominal; a participant may belong to more than one ingredient group if they reported multiple products |
| Age at screening | `RIDAGEYR` in `DEMO_L` | Descriptive or potential explanatory variable; also used to define adult eligibility | Quantitative, recorded in whole years; ratio scale |
| Sex category as recorded by NHANES | `RIAGENDR` in `DEMO_L` | Descriptive or potential grouping variable | Categorical, binary, nominal |
| Dietary Day 1 sample weight | `WTDRD1` in `DSQTOT_L` | Survey-weight variable for consideration in population estimates | Quantitative numerical weight; a sampling-design variable, not a health outcome |
| Survey stratum and primary sampling unit | `SDMVSTRA` and `SDMVPSU` in `DEMO_L` | Survey-design variables for variance estimation | Categorical design identifiers; they are not substantive health variables |
| Participant identifier | `SEQN` | Used to link participant files and check uniqueness | Identifier only; nominal label, not a quantitative analysis variable |

For the preliminary research question, sleep duration is the response (outcome) variable, and supplement-use status is the explanatory or grouping variable. Age and sex may be used to describe the analytic sample or to form descriptive subgroups. The project will not treat the participant identifier or survey-design identifiers as measured health characteristics.

The sleep-duration variables require special care. NHANES reports values of 2 as “less than 3 hours” and values of 14 as “14 hours or more.” Therefore, these endpoint values are grouped categories rather than exact sleep durations. They must not automatically be interpreted as exactly 2 or 14 hours in summaries that assume exact numeric values. Age is also top-coded at 80 years in the public-use file, so a recorded age of 80 may mean 80 years or older.

The final definition of the supplement exposure and the exact sample weight will be confirmed before the main analysis. The appropriate weight and survey-design variables will be justified in the NHANES-specific sampling and weighting section.