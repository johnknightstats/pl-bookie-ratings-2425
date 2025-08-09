
#########################################################
### Optimizer to get best ratings using 3-game window ###
#########################################################

import pandas as pd
import numpy as np
from scipy.optimize import minimize
from collections import defaultdict
import os

# === CONFIG ===
DATA_PATH = "../data/E0_with_handicap.csv"
OUTPUT_PATH = "../data/rolling_team_ratings.csv"
LOGO_PATH_TEMPLATE = "logos/{team}.png"

# === Load data ===
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values('Date').reset_index(drop=True)

# === Identify all teams and assign match indexes ===
teams = sorted(set(df['HomeTeam']).union(df['AwayTeam']))
team_matches = defaultdict(list)

# Track which matches each team played in
for idx, row in df.iterrows():
    team_matches[row['HomeTeam']].append(idx)
    team_matches[row['AwayTeam']].append(idx)

# Wait until all teams have played at least one match
min_start_date = max(df.loc[team_matches[t][0], 'Date'] for t in teams)

# List of all match dates after that point
match_dates = sorted(df[df['Date'] >= min_start_date]['Date'].unique())

# === Exclude final match date from rating calculation ===
match_dates = match_dates[:-1]

# === Estimate global home advantage ===
global_home_adv = df['Handicap_Pred'].mean()
print(f"Global home advantage: {global_home_adv:.4f}")

# === Rolling rating calculation ===
all_ratings = []

for current_date in match_dates:
    current_matches = df[df['Date'] == current_date]
    teams_today = set(current_matches['HomeTeam']).union(current_matches['AwayTeam'])
    used_match_idxs = set()

    for team in teams:
        match_ids = team_matches[team]
        match_dates_team = df.loc[match_ids, 'Date']
        idx_today = np.where(match_dates_team == current_date)[0]

        if len(idx_today) == 1:
            # Team is playing today → include this match plus ±1
            idx = idx_today[0]
            if idx > 0:
                used_match_idxs.add(match_ids[idx - 1])
            used_match_idxs.add(match_ids[idx])
            if idx < len(match_ids) - 1:
                used_match_idxs.add(match_ids[idx + 1])
        else:
            # Team is not playing → include prev and next matches
            match_dates_team = pd.Series(match_dates_team.values, index=range(len(match_ids)))
            future = match_dates_team[match_dates_team > current_date]
            past = match_dates_team[match_dates_team < current_date]

            if len(past) > 0:
                used_match_idxs.add(match_ids[past.index[-1]])
            if len(future) > 0:
                used_match_idxs.add(match_ids[future.index[0]])

    window_df = df.loc[list(used_match_idxs)].copy()

    # === Optimization step ===
    team_idx = {team: i for i, team in enumerate(teams)}
    n_teams = len(teams)

    def loss(params):
        ratings = params
        errors = []
        for _, row in window_df.iterrows():
            h = team_idx[row['HomeTeam']]
            a = team_idx[row['AwayTeam']]
            pred = ratings[h] - ratings[a] + global_home_adv
            errors.append((pred - row['Handicap_Pred']) ** 2)
        return np.mean(errors)

    x0 = np.zeros(n_teams)
    result = minimize(loss, x0, method="L-BFGS-B")

    if result.success:
        ratings = -result.x  # Flip: positive = stronger
        ratings -= ratings.mean()  # Center around 0
        for team in teams:
            all_ratings.append({
                'Date': current_date,
                'Team': team,
                'Rating': ratings[team_idx[team]]
            })
    else:
        print(f"Optimization failed on {current_date.date()}: {result.message}")

# === Create final ratings dataframe ===
ratings_df = pd.DataFrame(all_ratings)

# Add path to logo file (sanitized)
def make_logo_path(team):
    sanitized = team.replace(" ", "_").replace("'", "")
    return LOGO_PATH_TEMPLATE.format(team=sanitized)

ratings_df['LogoPath'] = ratings_df['Team'].apply(make_logo_path)

# Save
ratings_df.to_csv(OUTPUT_PATH, index=False)
print(f"Rolling team ratings saved to {OUTPUT_PATH}")



