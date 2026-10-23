"""Rebuild the NHANES Phase 1 adult sleep and supplement analysis outputs."""
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "processed" / "phase1"
FIGURES = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


def read_xpt(name):
    path = DATA / f"{name}.xpt"
    if not path.exists():
        raise FileNotFoundError(f"Required NHANES file not found: {path}")
    try:
        frame, meta = pyreadstat.read_xport(str(path), encoding="WINDOWS-1252")
    except UnicodeDecodeError:
        frame, meta = pyreadstat.read_xport(str(path), encoding="LATIN1")
    return frame, meta


def check_unique(frame, name):
    if frame["SEQN"].duplicated().any():
        raise ValueError(f"{name} has repeated SEQN values; review merge structure first")


def numeric_sleep(series):
    """Return valid numeric hours; NHANES 2 and 14 are grouped endpoint codes."""
    return series.where(series.between(3, 13.5))


def weighted_mean(values, weights):
    ok = values.notna() & weights.notna() & weights.gt(0)
    return float(np.average(values[ok], weights=weights[ok])) if ok.any() else np.nan


def save_distribution(frame, col, title, filename):
    vals = frame[col]
    valid = vals.notna()
    counts = vals[valid].value_counts().sort_index()
    labels = ["<3" if x == 2 else "14+" if x == 14 else f"{x:g}" for x in counts.index]
    pct = counts / counts.sum() * 100
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(labels, pct, color="#3978a8", edgecolor="white")
    ax.set_title(title)
    ax.set_xlabel("Usual sleep duration (hours; grouped endpoints shown as <3 and 14+)")
    ax.set_ylabel("Participants (%)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=.2)
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return counts, pct


def save_boxplot(frame, col, title, filename):
    d = frame[["DSD010", col]].copy()
    d["sleep_hours"] = numeric_sleep(d[col])
    d = d[d["sleep_hours"].notna() & d["DSD010"].isin([1, 2])]
    groups = [d.loc[d.DSD010.eq(code), "sleep_hours"].values for code in (2, 1)]
    names = [f"No supplement\n(n={len(groups[0]):,})", f"Any supplement\n(n={len(groups[1]):,})"]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.boxplot(groups, tick_labels=names, showfliers=False, patch_artist=True,
               medianprops={"color": "#222222", "linewidth": 1.5},
               boxprops={"facecolor": "#6baed6", "edgecolor": "#345"},
               whiskerprops={"color": "#345"}, capprops={"color": "#345"})
    ax.set_title(title)
    ax.set_ylabel("Usual sleep duration (hours; numeric values 3–13.5)")
    ax.set_xlabel("Self-reported dietary supplement use in past 30 days")
    ax.grid(axis="y", alpha=.2)
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return d


def main():
    demo, _ = read_xpt("DEMO_L")
    sleep, _ = read_xpt("SLQ_L")
    supp, supp_meta = read_xpt("DSQTOT_L")
    for f, n in ((demo, "DEMO_L"), (sleep, "SLQ_L"), (supp, "DSQTOT_L")):
        check_unique(f, n)
    flow = [{"step": "DEMO_L", "participants": int(demo.SEQN.nunique())}]
    merged = demo.merge(sleep, on="SEQN", how="inner", validate="one_to_one")
    flow.append({"step": "DEMO_L + SLQ_L", "participants": int(merged.SEQN.nunique())})
    merged = merged.merge(supp, on="SEQN", how="inner", validate="one_to_one")
    flow.append({"step": "DEMO_L + SLQ_L + DSQTOT_L", "participants": int(merged.SEQN.nunique())})
    adult = merged.loc[merged.RIDAGEYR.ge(20)].copy()
    flow.append({"step": "Age 20+", "participants": int(adult.SEQN.nunique())})
    adult.to_csv(OUT / "adult_merged.csv", index=False)

    # Preserve NHANES special response codes in frequencies; treat them as non-numeric sleep.
    exposure = adult.DSD010.isin([1, 2])
    exp = adult.loc[exposure].copy()
    exp["supplement_use"] = exp.DSD010.map({1: "Yes", 2: "No"})
    exp["weekday_hours"] = numeric_sleep(exp.SLD012)
    exp["weekend_hours"] = numeric_sleep(exp.SLD013)

    weighted_adults = exp.loc[exp.WTDRD1.gt(0)].copy()
    prevalence_yes = weighted_adults.DSD010.eq(1)
    prevalence_weight = weighted_adults.WTDRD1
    prevalence = pd.DataFrame([{"n_valid_yes_no": int(len(weighted_adults)),
        "yes_unweighted_n": int(prevalence_yes.sum()),
        "prevalence_unweighted_percent": float(prevalence_yes.mean() * 100),
        "prevalence_WTDRD1_weighted_percent": float(np.average(prevalence_yes.astype(float), weights=prevalence_weight) * 100)}])
    prevalence.to_csv(OUT / "supplement_prevalence.csv", index=False)
    summary_rows = []
    for outcome, label in (("weekday_hours", "Weekday/workday sleep"), ("weekend_hours", "Weekend/non-workday sleep")):
        for group, part in weighted_adults.groupby("supplement_use", sort=False):
            x = part[outcome].dropna()
            w = part.loc[x.index, "WTDRD1"]
            summary_rows.append({
                "outcome": label, "group": group, "n_valid": int(x.count()),
                "mean_unweighted_hours": float(x.mean()), "median_hours": float(x.median()),
                "q1_hours": float(x.quantile(.25)), "q3_hours": float(x.quantile(.75)),
                "mean_WTDRD1_weighted_hours": weighted_mean(x, w),
            })
    pd.DataFrame(summary_rows).to_csv(OUT / "sleep_by_supplement_summary.csv", index=False)

    count_rows = []
    for col, label in (("SLD012", "Weekday/workday"), ("SLD013", "Weekend/non-workday")):
        counts = adult[col].value_counts(dropna=False).sort_index()
        total_valid = adult[col].notna().sum()
        for value, n in counts.items():
            code = "Missing" if pd.isna(value) else "<3 hours (NHANES code 2)" if value == 2 else "14+ hours (NHANES code 14)" if value == 14 else f"{value:g} hours"
            count_rows.append({"measure": label, "response": code, "n": int(n), "percent_of_valid": float(n / total_valid * 100) if pd.notna(value) else np.nan})
    pd.DataFrame(count_rows).to_csv(OUT / "sleep_response_frequencies.csv", index=False)

    save_distribution(adult, "SLD012", "Usual weekday/workday sleep duration — adults aged 20+", "fig1_weekday_sleep_distribution.png")
    save_distribution(adult, "SLD013", "Usual weekend/non-workday sleep duration — adults aged 20+", "fig2_weekend_sleep_distribution.png")
    weekday_box = save_boxplot(exp, "SLD012", "Weekday/workday sleep by supplement-use status — adults aged 20+", "fig3_weekday_sleep_by_supplement.png")
    weekend_box = save_boxplot(exp, "SLD013", "Weekend/non-workday sleep by supplement-use status — adults aged 20+", "fig4_weekend_sleep_by_supplement.png")

    flow.append({"step": "Adults with valid yes/no DSD010", "participants": int(len(exp))})
    flow.append({"step": "Adults with positive WTDRD1 among valid yes/no", "participants": int(exp.WTDRD1.gt(0).sum())})
    pd.DataFrame(flow).to_csv(OUT / "merge_and_eligibility_flow.csv", index=False)
    # A small metadata record makes source versions and output scope explicit.
    metadata = {
        "source": "CDC/NCHS NHANES August 2021–August 2023",
        "files": ["DEMO_L.xpt", "SLQ_L.xpt", "DSQTOT_L.xpt"],
        "merge_key": "SEQN", "adult_rule": "RIDAGEYR >= 20",
        "supplement_yes_no_codes": {"1": "Yes", "2": "No"},
        "sleep_exact_numeric_rule": "3 <= sleep hours <= 13.5; codes 2 and 14 are grouped endpoints",
        "figures": sorted(p.name for p in FIGURES.glob("fig*.png")),
    }
    (OUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(pd.DataFrame(flow).to_string(index=False))
    print(f"\nAdult analysis rows with valid exposure: {len(exp):,}")
    print(f"Valid weekday comparisons: {len(weekday_box):,}; weekend comparisons: {len(weekend_box):,}")
    print(f"Outputs: {OUT}\nFigures: {FIGURES}")


if __name__ == "__main__":
    main()
