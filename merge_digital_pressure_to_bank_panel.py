import pandas as pd

bank = pd.read_csv("Academic_Bank_Panel_Data_Cleaned.csv")
digital = pd.read_csv("digital_payment_pressure_mobile_internet_banking.csv")

loc_map = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "PHL": "Philippines",
    "SGP": "Singapore",
    "THA": "Thailand"
}

bank["country"] = bank["loc"].map(loc_map)

merged = bank.merge(
    digital,
    on=["country", "fyear"],
    how="left"
)

merged.to_csv("bank_panel_with_digital_payment_pressure.csv", index=False)

print("Merged file saved as bank_panel_with_digital_payment_pressure.csv")

print("\nPreview:")
print(
    merged[["conm", "loc", "country", "fyear", "Digital_Payment_Pressure"]]
    .head(30)
    .to_string(index=False)
)

print("\nMissing Digital_Payment_Pressure:")
print(merged["Digital_Payment_Pressure"].isna().sum())

print("\nMissing by country:")
print(merged.groupby("country")["Digital_Payment_Pressure"].apply(lambda x: x.isna().sum()))