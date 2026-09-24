"""List candidate IMF FAS indicators for the digital-payment measure selection."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "02_Data"
INPUT_FILE = DATA_DIR / "01_Raw" / "IMF_FAS_Wide_Raw.csv"
OUTPUT_FILE = DATA_DIR / "02_Reference_and_Templates" / "FAS_Indicator_Keyword_Matches.csv"
KEYWORDS = ("mobile", "internet", "banking", "transaction", "transactions", "gdp")


def main() -> None:
    """Find and export FAS indicator labels matching the predefined keywords."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Missing {INPUT_FILE.name}. Run src/data/download_imf_fas.py first."
        )

    dataframe = pd.read_csv(INPUT_FILE, low_memory=False)
    labels = dataframe[["INDICATOR", "INDICATOR_LABEL"]].drop_duplicates()
    mask = pd.Series(False, index=labels.index)
    for keyword in KEYWORDS:
        mask |= labels["INDICATOR_LABEL"].astype(str).str.contains(
            keyword, case=False, na=False
        )

    matches = labels[mask].sort_values("INDICATOR_LABEL")
    matches.to_csv(OUTPUT_FILE, index=False)
    print(matches.to_string(index=False))
    print(f"\nWrote candidate indicators: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
