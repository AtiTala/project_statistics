## 2. Unit of Observation and Data Structure

A row represents one record, but the type of record depends on the file. The participant-level files have one row per respondent. The supplement-use file has one row per reported product or antacid, so one participant may appear in several rows. The supplement-reference files have rows for products, ingredients, or blend components.

| File | Rows in downloaded file | What one row represents | Repeated records? |
|---|---:|---|---|
| `DEMO_L` | 11,933 | One NHANES participant | No repeated `SEQN` values |
| `SLQ_L` | 8,501 | One participant’s sleep questionnaire record | No repeated `SEQN` values |
| `DSQTOT_L` | 8,860 | One participant’s total supplement-use record, including users and non-users | No repeated `SEQN` values |
| `DSQIDS_L` | 11,375 | One supplement or antacid reported by a participant | Yes. The file contains 4,017 distinct participants; 2,506 have multiple records, and one participant has up to 30 records |
| `DSPI` | 20,235 | One supplement product in the product-reference database | No repeated `DSDPID` values |
| `DSII` | 188,552 | One ingredient entry associated with a supplement product | Yes. A product may have many ingredient entries |
| `DSBI` | 37,061 | One component listed within a supplement blend | Yes. A blend may have many listed components |

For the main analysis, the **participant is the unit of observation**, because sleep duration is measured for each person. Before analysis, supplement reports must therefore be organized into participant-level exposure information. The product and ingredient files provide the detail needed to identify what was reported.

The files are connected through identifiers. `SEQN` identifies participants and connects the participant-level data to their supplement reports. `DSDPID` connects a reported supplement product to its product and ingredient information. `DSDIID` connects an ingredient that is a blend to the components listed for that blend.




Participant-level records
DEMO_L ─┐
SLQ_L  ─┼── SEQN ── DSQIDS_L: one row per reported product or antacid
DSQTOT_L┘                           │
                                    └── DSDPID ── DSPI: product information
                                                └── DSII: ingredient entries
                                                       │
                                                       └── DSDIID ── DSBI: blend components




The row counts differ across files because each file covers a different type of record and may have different eligibility or completion requirements. These differences do not, by themselves, indicate an error. Before analysis, the merge process and the number of participants retained at each step must be checked and reported.

Sources: CDC/NHANES documentation for [`DEMO_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm), [`SLQ_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/SLQ_L.htm), [`DSQIDS_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQIDS_L.htm), [`DSQTOT_L`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DSQTOT_L.htm), [`DSPI`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSPI.htm), [`DSII`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSII.htm), and [`DSBI`](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DSBI.htm).