#####################################################
### Regression to get precise handicaps from odds ###
#####################################################

import pandas as pd
import statsmodels.api as sm

# === Load data ===
df = pd.read_csv("../data/E0_clean.csv")

# Keep necessary columns
df = df[['Date', 'HomeTeam', 'AwayTeam', 'GoalDiff', 'AHh', 'PCAHH']].dropna()

# How much above or below the handicap line did the home team win?
df['Residual'] = df['GoalDiff'] - df['AHh']

# Regress residual on the home odds at the handicap line
X = df[['PCAHH']]
X = sm.add_constant(X)
y = df['Residual']

model = sm.OLS(y, X).fit()
print(model.summary())

# Use the model to predict the adjustment based on odds
df['Adjustment'] = model.predict(X)

# Final estimated team difference: original line + adjustment
df['Handicap_Pred'] = df['AHh'] + df['Adjustment']

# Save with necessary columns
df.to_csv("../data/E0_with_handicap.csv", index=False)
print("Regression complete and saved to ../data/E0_with_handicap.csv")
