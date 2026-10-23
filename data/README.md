# NHANES data files

## Official source and collection period

Participant files come from the U.S. National Health and Nutrition Examination Survey (NHANES), conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC). The participant-data cycle used here is **August 2021–August 2023**. NHANES is a cross-sectional survey of the U.S. civilian, noninstitutionalized population. Data and documentation are publicly available from the [official NHANES 2021–2023 page](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023).

**Download date recorded for this project:** 2026-10-20.

The files are downloadable public-use SAS transport (`.xpt`) files. NHANES data collection combines household interviews and examinations at Mobile Examination Centers; the exact mode and eligibility differ by component and are described in each component’s documentation. The dataset is not a clinical-trial sample.

## Required files

| File | Purpose | Role in the project |
|---|---|---|
| `DEMO_L.xpt` | Demographics, participant identifier, weights, and sample design | Defines age and provides `SEQN`, `SDMVSTRA`, and `SDMVPSU` |
| `SLQ_L.xpt` | Sleep questionnaire | Provides `SLD012` (weekday/workday sleep) and `SLD013` (weekend sleep) |
| `DSQTOT_L.xpt` | Total dietary supplement use | Provides `DSD010` (any supplement use) and `WTDRD1` |
| `DSQIDS_L.xpt` | Individual supplement reports over the past 30 days | Optional product-level exposure exploration; participants can have multiple rows |
| `DSPI.xpt` | Supplement product reference database | Product descriptions and product IDs |
| `DSII.xpt` | Supplement ingredient reference database | Ingredient descriptions and product/ingredient IDs |
| `DSBI.xpt` | Supplement blend reference database | Components of ingredient blends |

The three reference files (`DSPI`, `DSII`, `DSBI`) describe the broader NHANES Dietary Supplement Database and are not limited to participant records in the 2021–2023 cycle. They are optional for the primary “any supplement use” question.

## Rebuild the analytical data

1. Download the required XPT files from the official CDC/NCHS pages linked below and place them directly in this folder. Keep the original files unchanged.
2. From the project root, run `python src/phase1_analysis.py`.
3. The script reads `DEMO_L`, `SLQ_L`, and `DSQTOT_L`, checks uniqueness of `SEQN`, and performs one-to-one inner joins using `SEQN`.
4. It restricts the descriptive comparison to adults (`RIDAGEYR >= 20`) and valid yes/no `DSD010` records. For numeric sleep summaries it uses exact values from 3 through 13.5 hours; NHANES endpoint codes 2 and 14 are retained as grouped categories in frequency tables, not treated as exact hours.
5. Generated merged data and summary tables are written to `data/processed/phase1/`; four PNG figures are written to `figures/`.

The script records merge and eligibility counts in `merge_and_eligibility_flow.csv`. Results should be checked against the component-specific eligibility and weighting guidance before population-level interpretation.

## Access, sharing, and limitations

Raw `.xpt` files should remain unchanged and local. They are excluded from Git because they are source data files and may be large. Do not upload the raw files to GitHub; use this README, code, and CDC/NCHS source links to document retrieval and reconstruction. Generated processed files are also excluded from Git. No individual-level result should be interpreted as causal: the project uses cross-sectional observational survey data and self-reported measures.

## Official documentation

- [NHANES August 2021–August 2023 overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023)
- [Demographics (`DEMO_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm)
- [Sleep questionnaire (`SLQ_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm)
- [Total supplement use (`DSQTOT_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm)
- [Individual supplement use (`DSQIDS_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQIDS_L.htm)
- [Product information (`DSPI`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSPI.htm)
- [Ingredient information (`DSII`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSII.htm)
- [Blend information (`DSBI`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSBI.htm)
