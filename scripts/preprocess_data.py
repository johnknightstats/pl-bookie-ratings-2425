######################################################
### Some preprocessing after downloading data file ###
######################################################

import pandas as pd

INPUT_PATH = "../data/E0_raw.csv"
OUTPUT_PATH = "../data/E0_clean.csv"

cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'AHh', 'PCAHH', 'PCAHA']

df = pd.read_csv(INPUT_PATH, usecols=cols)
df = df.dropna()

# Convert date from UK format to datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Calculate goal difference
df['GoalDiff'] = df['FTHG'] - df['FTAG']

df.to_csv(OUTPUT_PATH, index=False)
print(f"Preprocessed data saved to {OUTPUT_PATH}")
