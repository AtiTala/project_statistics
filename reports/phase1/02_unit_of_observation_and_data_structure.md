## 2. Unit of Observation and Data Structure

The NHANES files used in this project do not all have the same row structure. Some files contain participant-level records, while others contain product or ingredient records.

| File | Rows in the downloaded file | What one row represents | Repeated identifiers in this file |
|---|---:|---|---|

| `DEMO_L` | 11,933 | One NHANES participant, identified by `SEQN` | None; `SEQN` is unique |
| `SLQ_L` | 8,501 | One participant’s sleep-questionnaire record | None; `SEQN` is unique |
| `DSQTOT_L` | 8,860 | One participant’s total supplement-use record | None; `SEQN` is unique |
| `DSQIDS_L` | 11,375 | One supplement or antacid product reported by a participant | Yes. There are 4,017 distinct participants; 2,506 have multiple product records, and one participant has up to 30 |
| `DSPI` | 20,235 | One supplement product in the product-reference file | None; `DSDPID` is unique |
| `DSII` | 188,552 | One ingredient entry associated with a supplement product | Yes. A product can have multiple ingredient entries |
| `DSBI` | 37,061 | One component entry associated with a supplement blend | Yes. A blend can have multiple component entries |

*The row counts above are counts in the downloaded files used for this project. They describe file records, not necessarily the number of participants eligible for the final analysis.*

### Unit of observation for the main analysis

The **participant is the unit of observation in the main analysis**. The research question concerns a person’s reported sleep duration in relation to that person’s supplement-use information. Therefore, the final analysis dataset should contain no more than one row per participant.

The `DSQIDS_L` file is different: each row represents a **reported product**, so one participant may appear on multiple rows. Before using these records to describe a participant’s supplement exposure, the product reports must be summarized at the participant level. The product and ingredient reference files help identify reported products and their ingredients; they are not additional participant observations.

### How the files relate

The participant files are linked using `SEQN`. Supplement product reports are linked to product and ingredient reference information using `DSDPID`; blend-component information is linked using `DSDIID`.

    DEMO_L ─┐
    SLQ_L   ├── SEQN ── participant-level analysis record
    DSQTOT_L┘                 │
                              └── SEQN ── DSQIDS_L
                                          one row per reported product
                                                  │
                                                DSDPID
                                                  │
                                      ┌───────────┴───────────┐
                                      DSPI                  DSII
                                                       ingredient entries
                                                             │
                                                           DSDIID
                                                             │
                                                            DSBI
                                                    blend-component entries

The row counts differ because the files describe different records and may cover different sets of participants or products. A direct merge of all files without checking their structure could create multiple rows for the same participant—for example, when a participant has several supplement records or a product has several ingredient records. The merge steps must therefore preserve the participant as the analysis unit, and the number of participants and rows should be checked before and after each merge.

Sources: CDC/NCHS documentation for [`DEMO_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm), [`SLQ_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm), [`DSQIDS_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQIDS_L.htm), [`DSQTOT_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm), [`DSPI`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSPI.htm), [`DSII`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSII.htm), and [`DSBI`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSBI.htm).