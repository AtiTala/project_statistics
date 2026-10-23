# Project Card

## Working title

**Usual Sleep Duration and Any Dietary Supplement Use Among U.S. Adults: NHANES August 2021–August 2023**

## Dataset and planned subset

The project uses the public NHANES August 2021–August 2023 cycle. The initial data scope is the participant-level intersection of `DEMO_L.xpt` (demographics and sample design), `SLQ_L.xpt` (sleep questionnaire), and `DSQTOT_L.xpt` (any supplement use and Day 1 dietary weight). The initial analytic population is adults aged 20 years or older with a valid yes/no answer to `DSD010` and a valid sleep-duration response for the outcome being summarized.

`DSQIDS_L.xpt` supports exploratory identification of individual reported products. `DSPI.xpt`, `DSII.xpt`, and `DSBI.xpt` are reference databases for product, ingredient, and blend descriptions. They are not required to define the primary broad exposure of any supplement use.

## Main statistical question

Among adults aged 20 years or older represented in NHANES August 2021–August 2023, how do the distributions of usual weekday/workday sleep duration and usual weekend/non-workday sleep duration compare between participants who reported using any dietary supplement in the past 30 days and participants who reported no dietary supplement use?

## Unit and population of interpretation

The analysis unit is one NHANES participant, identified by `SEQN`. Findings are intended to describe the corresponding U.S. civilian, noninstitutionalized adult population only when the appropriate NHANES weights and survey design are applied. Unweighted results describe the analyzed sample.

## Main variables

- Exposure/group: `DSD010`, any dietary supplement in the past 30 days (yes/no; categorical binary).
- Outcomes: `SLD012`, usual weekday/workday sleep hours, and `SLD013`, usual weekend/non-workday sleep hours (quantitative, recorded in hours, with grouped endpoint codes).
- Eligibility: `RIDAGEYR >= 20` from `DEMO_L`.
- Weight/design context: `WTDRD1` in `DSQTOT_L`; `SDMVSTRA` and `SDMVPSU` in `DEMO_L`. The weight is appropriate only for analyses aligned with the Day 1 dietary component; design-based inference also requires the survey design variables.

## Question type and initial expectation

The primary question is descriptive and comparative. No directional difference is assumed. The project does not claim that supplements cause changes in sleep. “Any supplement” is a broad exposure and does not identify product, dose, or reason for use.

## Anticipated limitations

The data are cross-sectional and self-reported; supplement use aggregates many products; sleep values at the low and high ends are grouped rather than exact; missing responses reduce outcome-specific sample sizes; and the effective sample for any specific ingredient may be small. Survey weighting and design need to be matched to each estimate.

## Reproducibility

Run `python src/phase1_analysis.py` after installing `requirements.txt` and placing the source XPT files listed in `data/README.md` in `data/`. Generated analytic files are written under `data/processed/phase1/`, and figures are written under `figures/`.
