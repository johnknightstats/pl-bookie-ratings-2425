########################################################
### Get PL 2024-2025 data from Football-Data website ###
########################################################

import pandas as pd

URL = "https://www.football-data.co.uk/mmz4281/2425/E0.csv"
OUTPUT_PATH = "../data/E0_raw.csv"

df = pd.read_csv(URL)
df.to_csv(OUTPUT_PATH, index=False)
print(f"Downloaded and saved to {OUTPUT_PATH}")
