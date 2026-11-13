from pathlib import Path
import json

import pyreadstat


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "processed"
LABELS_DIR = OUTPUT_DIR / "labels"

xpt_files = sorted(DATA_DIR.glob("*.xpt"))

if not xpt_files:
    raise FileNotFoundError(f"No .xpt files found in: {DATA_DIR}")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LABELS_DIR.mkdir(parents=True, exist_ok=True)

for xpt_path in xpt_files:
    print(f"Reading {xpt_path.name}...")

    try:
        data, metadata = pyreadstat.read_xport(
            str(xpt_path),
            encoding="WINDOWS-1252",
        )
    except UnicodeDecodeError:
        data, metadata = pyreadstat.read_xport(
            str(xpt_path),
            encoding="LATIN1",
        )

    csv_path = OUTPUT_DIR / f"{xpt_path.stem}.csv"
    labels_path = LABELS_DIR / f"{xpt_path.stem}_labels.json"

    data.to_csv(csv_path, index=False) # type: ignore

    with labels_path.open("w", encoding="utf-8") as file:
        json.dump(
            metadata.column_names_to_labels,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"  Saved {data.shape[0]:,} rows, {data.shape[1]} columns") # type: ignore
    print(f"  Csv: {csv_path.name}")
    print(f"  Labels:  {labels_path.name}")

print(f"\nDone. Processed files are in: {OUTPUT_DIR}")