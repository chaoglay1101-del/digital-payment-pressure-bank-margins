"""Download the public IMF Financial Access Survey wide-format source file."""

from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
SOURCE_URL = "https://data360files.worldbank.org/data360-data/data/IMF_FAS/IMF_FAS_WIDEF.csv"
OUTPUT_FILE = ROOT / "IMF_FAS_WIDEF_raw.csv"


def main() -> None:
    """Retrieve and save the IMF FAS source data for local research use."""
    print("Downloading IMF FAS wide-format data...")
    response = requests.get(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=120,
    )
    response.raise_for_status()

    dataframe = pd.read_csv(StringIO(response.text), low_memory=False)
    dataframe.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {OUTPUT_FILE.name}: {dataframe.shape[0]} rows, {dataframe.shape[1]} columns")


if __name__ == "__main__":
    main()
