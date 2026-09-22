import pandas as pd

# Load raw FAS file
df = pd.read_csv("IMF_FAS_WIDEF_raw.csv", low_memory=False)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Show unique indicator labels that contain useful keywords
labels = df[["INDICATOR", "INDICATOR_LABEL"]].drop_duplicates()

keywords = [
    "mobile",
    "internet",
    "banking",
    "transaction",
    "transactions",
    "GDP",
    "gdp",
]

mask = pd.Series(False, index=labels.index)

for kw in keywords:
    mask = mask | labels["INDICATOR_LABEL"].astype(str).str.contains(kw, case=False, na=False)

matches = labels[mask].sort_values(["INDICATOR_LABEL"])

print("\nMatched indicators:")
print(matches.to_string(index=False))

matches.to_csv("fas_indicator_keyword_matches.csv", index=False)

print("\nSaved as fas_indicator_keyword_matches.csv")