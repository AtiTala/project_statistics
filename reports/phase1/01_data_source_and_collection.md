# Data Documentation

## Project data source

Participant data come from the U.S. National Health and Nutrition Examination Survey (NHANES), conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC).

The participant-data cycle used in this project is **August 2021–August 2023**. NHANES is a cross-sectional survey of the U.S. civilian, noninstitutionalized population. Official data and documentation are publicly available from the [NHANES 2021–2023 website](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023).

**Download date:** 2026-10-20  

## Files needed for this project

| File | What it contains |
|---|---|
| `DEMO_L.xpt` | Participant demographics and NHANES sample-design and weight variables. |
| `SLQ_L.xpt` | Self-reported usual sleep and wake times, including derived weekday and weekend sleep-duration variables. |
| `DSQIDS_L.xpt` | Individual supplement or antacid products reported during the 30 days before the interview. A participant may have multiple rows. |
| `DSQTOT_L.xpt` | Participant-level summary of supplement and antacid use, including users and non-users. It also contains the dietary Day 1 sample weight, `WTDRD1`. |
| `DSPI.xpt` | Reference information about supplement products. |
| `DSII.xpt` | Reference information about ingredients listed for supplement products. |
| `DSBI.xpt` | Reference information about ingredients listed within supplement blends. |

The `DSPI`, `DSII`, and `DSBI` files are product-reference files covering products in the NHANES Dietary Supplement Database, not participant records limited to the 2021–2023 cycle. Their records are linked to reported supplements using product and ingredient IDs.

## Rebuilding the analysis dataset

1. Read the original `.xpt` files from this folder.
2. Use `SEQN` (the respondent sequence number) to connect participant-level data from `DEMO_L`, `SLQ_L`, and `DSQTOT_L`.
3. Connect reported supplement products in `DSQIDS_L` to product and ingredient information using `DSDPID`. Connect blend information using `DSDIID`.
4. Check row counts, repeated participant records, missing values, and merge results before analysis.
5. Apply and document the final eligibility rules, including the adult age range, before producing analysis results.

NHANES recommends using the appropriate sample weights and survey-design information for population estimates. The analysis plan will document the selected weight and design variables before statistical analysis.

## Data access and sharing

The `.xpt` files are raw source data and should remain unchanged. Keep them in this local `data/` folder. Do not upload the large data files to GitHub; use this README, the analysis code, and official source links to document where the data came from and how to rebuild the analysis dataset.

## Official documentation

- [NHANES August 2021–August 2023 overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023)
- [Demographics and sample weights (`DEMO_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm)
- [Sleep questionnaire (`SLQ_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm)
- [Individual supplements (`DSQIDS_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQIDS_L.htm)
- [Total supplements (`DSQTOT_L`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm)
- [Product information (`DSPI`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSPI.htm)
- [Ingredient information (`DSII`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSII.htm)
- [Blend information (`DSBI`)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSBI.htm)