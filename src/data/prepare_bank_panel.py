"""Prepare a restricted WRDS-derived ASEAN bank panel for the research analysis.

The required source CSV and bank list are not distributed with this public portfolio.
"""

from pathlib import Path
import re
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "02_Data"
WRDS_INPUT = DATA_DIR / "01_Raw" / "ASEAN5_Banks_Panel_Raw.csv"
BANK_LIST_INPUT = DATA_DIR / "01_Raw" / "ASEAN5_Listed_Commercial_Banks.xlsx"
OUTPUT_FILE = DATA_DIR / "03_Intermediate" / "ASEAN5_Bank_Panel_Cleaned.csv"


def simplify_name(name: object) -> str:
    """Normalise a bank name before matching it to the supplied bank list."""
    if pd.isna(name):
        return ""

    simplified = re.sub(r"\(.*?\)", "", str(name).upper())
    for word in [
        " LTD",
        " BHD",
        " BERHAD",
        " CORP",
        " CORPORATION",
        " INC",
        " PLC",
        " PT",
        " TBK",
        ",",
        ".",
        "-",
    ]:
        simplified = simplified.replace(word, " ")
    return " ".join(simplified.split())


def main() -> None:
    """Filter the restricted bank data and construct financial analysis variables."""
    missing_inputs = [path for path in (WRDS_INPUT, BANK_LIST_INPUT) if not path.exists()]
    if missing_inputs:
        names = ", ".join(path.name for path in missing_inputs)
        raise FileNotFoundError(
            f"Missing restricted input file(s): {names}. These files are intentionally "
            "excluded from the public repository."
        )

    print("Loading restricted bank panel and bank list...")
    df_wrds = pd.read_csv(WRDS_INPUT, low_memory=False)
    df_excel = pd.read_excel(BANK_LIST_INPUT)

    bank_name_col = next(
        (col for col in df_excel.columns if "name" in str(col).lower() or "bank" in str(col).lower()),
        df_excel.columns[1],
    )

    asean5_codes = ["SGP", "MYS", "THA", "IDN", "PHL"]
    df_wrds = df_wrds[
        df_wrds["fic"].isin(asean5_codes) | df_wrds["loc"].isin(asean5_codes)
    ].copy()

    df_wrds["simple_name"] = df_wrds["conm"].apply(simplify_name)
    df_excel["simple_name"] = df_excel[bank_name_col].apply(simplify_name)

    matched_names: set[str] = set()
    for excel_name in df_excel["simple_name"]:
        words = excel_name.split()
        if not words:
            continue
        if words[0] == "BANK" and len(words) >= 3:
            search_key = " ".join(words[:3])
        elif len(words) >= 2:
            search_key = " ".join(words[:2])
        else:
            search_key = words[0]
        matched_names.update(
            name for name in df_wrds["simple_name"].unique() if search_key in str(name)
        )

    df_filtered = df_wrds[df_wrds["simple_name"].isin(matched_names)].copy()
    academic_cols = [
        "gvkey", "conm", "loc", "fic", "fyear", "datadate", "curcd", "indfmt",
        "revt", "idit", "xint", "initb", "bcef", "cfo", "ib", "ni", "pcl",
        "at", "che", "ivst", "custadv", "liqresn", "intan", "ppent", "dptb",
        "dptc", "dltt", "ceq", "seq", "lct", "txp",
    ]
    keep_cols = [column for column in academic_cols if column in df_filtered.columns]
    df_final = df_filtered[keep_cols].copy()

    identifier_cols = {"gvkey", "conm", "loc", "fic", "datadate", "curcd", "indfmt"}
    for column in [column for column in keep_cols if column not in identifier_cols]:
        df_final[column] = pd.to_numeric(df_final[column], errors="coerce")

    for column in ["pcl", "bcef", "cfo", "ivst", "liqresn", "initb"]:
        if column in df_final.columns:
            df_final[column] = df_final[column].fillna(0)

    before_drop = len(df_final)
    if "at" in df_final.columns:
        df_final = df_final.dropna(subset=["at"])

    if {"che", "at"}.issubset(df_final.columns):
        df_final["Liquidity_Ratio_LC1"] = df_final["che"] / df_final["at"]
    if {"custadv", "dptb"}.issubset(df_final.columns):
        df_final["L_D_Ratio"] = df_final["custadv"] / df_final["dptb"]
    if {"ceq", "at"}.issubset(df_final.columns):
        df_final["Capital_Adequacy_Proxy"] = df_final["ceq"] / df_final["at"]
    if {"initb", "at"}.issubset(df_final.columns):
        df_final["Net_Fee_Margin"] = df_final["initb"] / df_final["at"]

    sort_cols = [column for column in ["fic", "loc", "conm", "fyear"] if column in df_final.columns]
    df_final = df_final.sort_values(by=sort_cols)
    df_final.to_csv(OUTPUT_FILE, index=False)

    print(f"Removed {before_drop - len(df_final)} rows without total assets.")
    print(f"Wrote cleaned restricted panel: {OUTPUT_FILE.name} ({len(df_final)} rows)")


if __name__ == "__main__":
    main()
