"""Rebuild empirical event probabilities for NHANES Phase 2, tasks 1-3."""
from pathlib import Path
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "processed" / "phase2"
OUT.mkdir(parents=True, exist_ok=True)


def read_xpt(name: str) -> pd.DataFrame:
    path = DATA / f"{name}.xpt"
    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")
    try:
        frame, _ = pyreadstat.read_xport(str(path), encoding="WINDOWS-1252", output_format="pandas")
    except UnicodeDecodeError:
        frame, _ = pyreadstat.read_xport(str(path), encoding="LATIN1", output_format="pandas")
    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame from {path}")
    return frame


def require_unique_seqn(frame: pd.DataFrame, name: str) -> None:
    seqn = frame["SEQN"]
    if not isinstance(seqn, pd.Series) or seqn.hasnans or not seqn.is_unique:
        raise ValueError(f"{name} must contain one non-missing row per SEQN")


def main() -> None:
    demo = read_xpt("DEMO_L")
    sleep = read_xpt("SLQ_L")
    supplements = read_xpt("DSQTOT_L")
    for frame, name in ((demo, "DEMO_L"), (sleep, "SLQ_L"), (supplements, "DSQTOT_L")):
        require_unique_seqn(frame, name)

    merged = demo.merge(sleep, on="SEQN", how="inner", validate="one_to_one")
    merged = merged.merge(supplements, on="SEQN", how="inner", validate="one_to_one")
    adults = merged.loc[merged["RIDAGEYR"].ge(20)].copy()

    # A valid analysis record needs both a yes/no supplement response and a
    # non-missing SLD012 value. NHANES code 2 means <3 hours; code 14 means 14+.
    sample = adults.loc[
        adults["DSD010"].isin([1, 2]) & adults["SLD012"].notna()
    ].copy()
    if sample.empty:
        raise ValueError("No valid adult records remain for the probability analysis")

    sample["A_supplement_use"] = sample["DSD010"].eq(1)
    sample["B_weekday_sleep_under_7h"] = sample["SLD012"].lt(7)
    n = len(sample)

    event_counts = {
        "A: any supplement use": int(sample["A_supplement_use"].sum()),
        "B: weekday sleep <7 hours": int(sample["B_weekday_sleep_under_7h"].sum()),
        "A and B": int((sample["A_supplement_use"] & sample["B_weekday_sleep_under_7h"]).sum()),
    }
    marginal_joint = pd.DataFrame([
        {"quantity": label, "count": count, "denominator_n": n,
         "empirical_probability": count / n, "percent": 100 * count / n}
        for label, count in event_counts.items()
    ])
    marginal_joint.to_csv(OUT / "marginal_and_joint_probabilities.csv", index=False)

    contingency = pd.crosstab(
        sample["A_supplement_use"], sample["B_weekday_sleep_under_7h"],
        rownames=["A_any_supplement"], colnames=["B_weekday_sleep_under_7h"],
        dropna=False,
    ).reindex(index=[False, True], columns=[False, True], fill_value=0)
    joint = contingency.rename(index={False: "A complement: no", True: "A: yes"},
                               columns={False: "B complement: no", True: "B: yes"})
    joint.to_csv(OUT / "event_contingency_counts.csv")
    (joint / n).to_csv(OUT / "event_contingency_probabilities.csv")

    conditional = pd.DataFrame([
        {
            "condition": "Any supplement use",
            "group_n": int(sample["A_supplement_use"].sum()),
            "under_7h_n": int((sample["A_supplement_use"] & sample["B_weekday_sleep_under_7h"]).sum()),
        },
        {
            "condition": "No supplement use",
            "group_n": int((~sample["A_supplement_use"]).sum()),
            "under_7h_n": int((~sample["A_supplement_use"] & sample["B_weekday_sleep_under_7h"]).sum()),
        },
    ])
    conditional["conditional_probability"] = conditional["under_7h_n"] / conditional["group_n"]
    conditional["percent"] = 100 * conditional["conditional_probability"]
    conditional.to_csv(OUT / "conditional_probabilities.csv", index=False)

    print(f"Probability analysis set: {n:,} adults")
    print("Marginal and joint event probabilities:")
    print(marginal_joint.to_string(index=False, formatters={
        "empirical_probability": "{:.4f}".format, "percent": "{:.2f}%".format
    }))
    print("\nJoint event table (counts):")
    print(joint.to_string())
    print("\nConditional probabilities of weekday sleep under 7 hours:")
    print(conditional.to_string(index=False, formatters={
        "conditional_probability": "{:.4f}".format, "percent": "{:.2f}%".format
    }))
    print(f"\nSaved tables under: {OUT}")


if __name__ == "__main__":
    main()
