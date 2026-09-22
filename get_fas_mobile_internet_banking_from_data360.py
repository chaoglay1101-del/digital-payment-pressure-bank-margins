import pandas as pd
import requests
from io import StringIO

url = "https://data360files.worldbank.org/data360-data/data/IMF_FAS/IMF_FAS_WIDEF.csv"

print("Downloading IMF FAS wide file from Data360...")

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, timeout=120)
response.raise_for_status()

df = pd.read_csv(StringIO(response.text), low_memory=False)

print("Downloaded successfully.")
print("Shape:", df.shape)
print("Columns:")
print(df.columns.tolist()[:50])

df.to_csv("IMF_FAS_WIDEF_raw.csv", index=False)

print("\nSaved raw file as IMF_FAS_WIDEF_raw.csv")