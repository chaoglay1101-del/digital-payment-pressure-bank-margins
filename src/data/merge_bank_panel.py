"""Merge the restricted bank panel with the extracted country-year payment indicator."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "02_Data"
BANK_INPUT = DATA_DIR / "03_Intermediate" / "ASEAN5_Bank_Panel_Cleaned.csv"
DIGITAL_INPUT = DATA_DIR / "03_Intermediate" / "ASEAN5_Digital_Payment_Pressure.csv"
OUTPUT_FILE = DATA_DIR / "03_Intermediate" / "ASEAN5_Bank_Panel_Digital_Payment_Pressure.csv"
COUNTRY_NAMES = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "PHL": "Philippines",
    "SGP": "Singapore",
    "THA": "Thailand",
}


def main() -> None:
    """Join country-year digital-payment pressure to each bank-year observation."""
    missing_inputs = [path for path in (BANK_INPUT, DIGITAL_INPUT) if not path.exists()]
    if missing_inputs:
        names = ", ".join(path.name for path in missing_inputs)
        raise FileNotFoundError(
            f"Missing input file(s): {names}. The cleaned bank panel is restricted; the digital "
            "indicator can be generated with src/data/extract_digital_payment_pressure.py."
        )

    bank = pd.read_csv(BANK_INPUT)
    digital = pd.read_csv(DIGITAL_INPUT)
    if digital.duplicated(["country", "fyear"]).any():
        raise ValueError("Digital-payment data must contain one observation per country-year.")

    bank["country"] = bank["loc"].map(COUNTRY_NAMES)
    merged = bank.merge(digital, on=["country", "fyear"], how="left", validate="many_to_one")
    merged.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote merged panel: {OUTPUT_FILE.name} ({len(merged)} rows)")
    print("Missing digital-payment observations:", merged["Digital_Payment_Pressure"].isna().sum())


if __name__ == "__main__":
    main()
