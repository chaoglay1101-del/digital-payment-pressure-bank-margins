import pandas as pd

# Load raw FAS file
df = pd.read_csv("IMF_FAS_WIDEF_raw.csv", low_memory=False)

target_indicator = "IMF_FAS_FCMIBT"

countries = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "PHL": "Philippines",
    "SGP": "Singapore",
    "THA": "Thailand",
}

# Keep only the percentage of GDP measure
sub = df[
    (df["INDICATOR"] == target_indicator)
    & (df["REF_AREA"].isin(countries.keys()))
    & (df["UNIT_MEASURE"] == "PT_GDP")
].copy()

print("Selected rows:")
print(
    sub[
        [
            "REF_AREA",
            "REF_AREA_LABEL",
            "INDICATOR",
            "INDICATOR_LABEL",
            "UNIT_MEASURE",
            "UNIT_MEASURE_LABEL",
        ]
    ]
    .drop_duplicates()
    .to_string(index=False)
)

# Detect year columns
year_cols = [c for c in sub.columns if str(c).isdigit()]

long = sub.melt(
    id_vars=[
        "REF_AREA",
        "REF_AREA_LABEL",
        "INDICATOR",
        "INDICATOR_LABEL",
        "UNIT_MEASURE",
        "UNIT_MEASURE_LABEL",
    ],
    value_vars=year_cols,
    var_name="fyear",
    value_name="Digital_Payment_Pressure"
)

long["fyear"] = long["fyear"].astype(int)

long["Digital_Payment_Pressure"] = pd.to_numeric(
    long["Digital_Payment_Pressure"],
    errors="coerce"
)

long = long[(long["fyear"] >= 2014) & (long["fyear"] <= 2023)]

long["country"] = long["REF_AREA"].map(countries)

final = long[["country", "fyear", "Digital_Payment_Pressure"]].copy()

final = final.sort_values(["country", "fyear"])

final.to_csv("digital_payment_pressure_mobile_internet_banking.csv", index=False)

print("\nFinal extracted data:")
print(final.to_string(index=False))

print("\nRows:", len(final))

print("\nDuplicated country-year:")
print(final[final.duplicated(["country", "fyear"], keep=False)].to_string(index=False))

print("\nMissing values by country:")
print(final.groupby("country")["Digital_Payment_Pressure"].apply(lambda x: x.isna().sum()))

print("\nSaved as digital_payment_pressure_mobile_internet_banking.csv")