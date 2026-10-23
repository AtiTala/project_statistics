# Sleep Duration and Dietary Supplement Use in NHANES

This project uses the U.S. National Health and Nutrition Examination Survey (NHANES), August 2021–August 2023 cycle, to describe and compare usual weekday/workday and weekend/non-workday sleep duration between adults who reported any dietary supplement use in the past 30 days and adults who reported none.

The project is a descriptive analysis of cross-sectional survey data. It does not estimate a causal effect. The broad exposure combines all dietary supplements and cannot identify a specific product, dose, or reason for use.

## Project structure

- `PROJECT_CARD.md` — statistical scope and current research question.
- `data/README.md` — official sources, files, download details, and rebuild instructions.
- `data/` — local raw NHANES XPT files; these are excluded from Git.
- `notebooks/01_inspect_data.ipynb` — guided, runnable review of the Phase 1 analysis and outputs.
- `src/phase1_analysis.py` — reproducible merge, eligibility, descriptive summaries, and figures.
- `data/processed/phase1/` — generated tables and merged analytic data; excluded from Git.
- `figures/` — four generated Phase 1 figures.
- `reports/phase1/` — individual Phase 1 report sections and Path A appendices.
- `reports/phase1.pdf` — integrated Phase 1 report.

## Reproduce Phase 1

1. Install Python 3.10 or newer.
2. From the project folder, create and activate a virtual environment if desired.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Download the seven files listed in `data/README.md` into `data/`.
5. Open `notebooks/01_inspect_data.ipynb` in VS Code and choose **Run All** to rebuild the tables and figures and review their outputs. You can also run `python src/phase1_analysis.py` from the project folder.
6. Run `python src/build_phase1_pdf.py` to regenerate `reports/phase1.pdf` from the report sections and figures.

The script joins `DEMO_L`, `SLQ_L`, and `DSQTOT_L` one-to-one using `SEQN`, restricts the descriptive comparison to adults aged 20 years or older, preserves the NHANES grouped sleep endpoints, and writes processed tables plus four figures. Raw XPT files are read without modification.

## Phase 1 interpretation

The preliminary unweighted medians were 8 hours in both supplement-use groups for both sleep outcomes. The report presents the full distributions and compares raw with WTDRD1-weighted means. NHANES weights and design variables must be selected to match the estimand and component eligibility; weighted summaries are not interchangeable with design-based standard errors or tests.

See `reports/phase1.pdf` for the integrated report and `reports/phase1/` for its source sections. Official dataset documentation is linked in `data/README.md`.
