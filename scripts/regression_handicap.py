#####################################################
### Regression to get precise handicaps from odds ###
#####################################################

import pandas as pd
import statsmodels.api as sm

# Load data
df = pd.read_csv("../data/E0_clean.csv")

# Regression: GoalDiff ~ PCAHH only
X = df[['PCAHH']]
X = sm.add_constant(X)
y = df['GoalDiff']

model = sm.OLS(y, X).fit()
print(model.summary())

# Adjustment learned from PCAHH
df['Adjustment'] = model.predict(X)

# Final estimated team difference: original line + adjustment
df['Handicap_Pred'] = df['AHh'] + df['Adjustment']

# Save to file
df.to_csv("../data/E0_with_handicap.csv", index=False)
print("✅ Regression complete and saved to ../data/E0_with_handicap.csv")

