"""Extract the selected IMF FAS digital-payment indicator into country-year form."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "02_Data"
INPUT_FILE = DATA_DIR / "01_Raw" / "IMF_FAS_Wide_Raw.csv"
OUTPUT_FILE = DATA_DIR / "03_Intermediate" / "ASEAN5_Digital_Payment_Pressure.csv"
TARGET_INDICATOR = "IMF_FAS_FCMIBT"
COUNTRIES = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "PHL": "Philippines",
    "SGP": "Singapore",
    "THA": "Thailand",
}


def main() -> None:
    """Create the digital-payment-pressure country-year data used by the pipeline."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Missing {INPUT_FILE.name}. Run src/data/download_imf_fas.py first."
        )

    dataframe = pd.read_csv(INPUT_FILE, low_memory=False)
    selected = dataframe[
        (dataframe["INDICATOR"] == TARGET_INDICATOR)
        & dataframe["REF_AREA"].isin(COUNTRIES)
        & (dataframe["UNIT_MEASURE"] == "PT_GDP")
    ].copy()
    if selected.empty:
        raise ValueError(
            f"No {TARGET_INDICATOR} observations with unit PT_GDP were found in {INPUT_FILE.name}."
        )

    year_columns = [column for column in selected.columns if str(column).isdigit()]
    long = selected.melt(
        id_vars=[
            "REF_AREA",
            "REF_AREA_LABEL",
            "INDICATOR",
            "INDICATOR_LABEL",
            "UNIT_MEASURE",
            "UNIT_MEASURE_LABEL",
        ],
        value_vars=year_columns,
        var_name="fyear",
        value_name="Digital_Payment_Pressure",
    )
    long["fyear"] = long["fyear"].astype(int)
    long["Digital_Payment_Pressure"] = pd.to_numeric(
        long["Digital_Payment_Pressure"], errors="coerce"
    )
    long = long[long["fyear"].between(2014, 2023)]
    long["country"] = long["REF_AREA"].map(COUNTRIES)

    final = long[["country", "fyear", "Digital_Payment_Pressure"]].sort_values(
        ["country", "fyear"]
    )
    if final.duplicated(["country", "fyear"]).any():
        raise ValueError("The selected FAS measure contains duplicate country-year observations.")

    final.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote digital payment indicator: {OUTPUT_FILE.name} ({len(final)} rows)")
    print(final.groupby("country")["Digital_Payment_Pressure"].apply(lambda values: values.isna().sum()))


if __name__ == "__main__":
    main()
