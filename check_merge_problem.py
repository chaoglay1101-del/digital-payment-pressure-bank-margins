import pandas as pd

bank = pd.read_csv("Academic_Bank_Panel_Data_Cleaned.csv")
digital = pd.read_csv("digital_payment_pressure_mobile_internet_banking.csv")
merged = pd.read_csv("bank_panel_with_digital_payment_pressure.csv")

print("Bank panel rows:", len(bank))
print("Digital pressure rows:", len(digital))
print("Merged rows:", len(merged))

print("\nBank unique gvkey-year:")
print(bank[["gvkey", "fyear"]].drop_duplicates().shape[0])

print("\nMerged unique gvkey-year:")
print(merged[["gvkey", "fyear"]].drop_duplicates().shape[0])

print("\nDuplicated country-year in digital file:")
dup = digital[digital.duplicated(["country", "fyear"], keep=False)]
print(dup.sort_values(["country", "fyear"]).to_string(index=False))

print("\nCount per country-year in digital file:")
print(
    digital.groupby(["country", "fyear"])
    .size()
    .reset_index(name="count")
    .query("count > 1")
    .to_string(index=False)
)

print("\nMissing Digital Payment Pressure in merged file:")
print(merged["Digital_Payment_Pressure"].isna().sum())

print("\nMerged rows by country:")
print(merged.groupby("country").size())