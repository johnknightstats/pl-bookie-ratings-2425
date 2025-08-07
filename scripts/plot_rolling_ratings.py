
##########################################################
### Plot time series of all teams' ratings over season ###
##########################################################

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from statsmodels.nonparametric.smoothers_lowess import lowess

# === CONFIG ===
INPUT_PATH = "../data/rolling_team_ratings.csv"
OUTPUT_HTML = "../viz/rolling_team_ratings.html"
LOESS_FRACTION = 0.15  # Smoothing parameter

# Team colors (custom)
team_colors = {
    "Arsenal": "yellow",
    "Aston Villa": "darkred",
    "Bournemouth": "red",
    "Brentford": "lime",
    "Brighton": "blue",
    "Chelsea": "blue",
    "Crystal Palace": "deeppink",
    "Everton": "blue",
    "Fulham": "black",
    "Ipswich": "magenta",
    "Leicester": "blue",
    "Liverpool": "red",
    "Man City": "skyblue",
    "Man United": "yellow",
    "Newcastle": "black",
    "Nott'm Forest": "green",
    "Southampton": "red",
    "Tottenham": "white",
    "West Ham": "darkred",
    "Wolves": "gold"
}

# === Load data ===
df = pd.read_csv(INPUT_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# === Apply LOESS smoothing ===
smoothed_rows = []

for team in df['Team'].unique():
    team_df = df[df['Team'] == team].sort_values('Date')
    if len(team_df) >= 5:
        smoothed = lowess(endog=team_df['Rating'], exog=team_df['Date'].astype(int), frac=LOESS_FRACTION, return_sorted=False)
        team_df['SmoothedRating'] = smoothed
    else:
        team_df['SmoothedRating'] = team_df['Rating']
    smoothed_rows.append(team_df)

plot_df = pd.concat(smoothed_rows)

# === Plot with individual traces to control hover ===
fig = go.Figure()

for team in plot_df['Team'].unique():
    team_data = plot_df[plot_df['Team'] == team]
    fig.add_trace(go.Scatter(
        x=team_data['Date'],
        y=team_data['SmoothedRating'],
        mode='lines',
        name=team,
        line=dict(color=team_colors.get(team, 'grey'), width=2),
        hovertemplate=(
            "<b>%{text}</b><br>" +
            "Rating: %{y:.2f}<br>" +
            "Date: %{x|%b %d, %Y}<extra></extra>"
        ),
        text=[team] * len(team_data),
        showlegend=True
    ))


fig.update_layout(
    title="Bookmaker-Derived Premier League Ratings 2024-2025",
    plot_bgcolor="lightgrey",
    template="simple_white",
    hovermode="closest",
    legend=dict(title="Team", orientation="v", x=1.01, y=1),
    margin=dict(r=140)
)

# Save
os.makedirs("../viz", exist_ok=True)
fig.write_html(OUTPUT_HTML)
print(f"✅ Interactive rolling ratings plot saved to {OUTPUT_HTML}")



