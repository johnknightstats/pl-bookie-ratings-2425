
##########################################################
### Plot time series of all teams' ratings over season ###
##########################################################

import os
from math import floor, ceil
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess

# === CONFIG ===
INPUT_PATH = "../data/rolling_team_ratings.csv"
OUTPUT_HTML = "../viz/rolling_team_ratings.html"
LOESS_FRACTION = 0.2  

# Team colors
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
df["Date"] = pd.to_datetime(df["Date"])

# === Apply LOESS smoothing per team ===
frames = []
for team in df["Team"].unique():
    tdf = df[df["Team"] == team].sort_values("Date").copy()
    if len(tdf) >= 5:
        # Convert datetime to int64 nanoseconds for lowess exog
        x_numeric = tdf["Date"].view("int64")
        tdf["SmoothedRating"] = lowess(
            endog=tdf["Rating"],
            exog=x_numeric,
            frac=LOESS_FRACTION,
            return_sorted=False
        )
    else:
        tdf["SmoothedRating"] = tdf["Rating"]
    frames.append(tdf)

plot_df = pd.concat(frames, ignore_index=True)

# === Build the figure (one trace per team for clean hover) ===
fig = go.Figure()

for team in plot_df["Team"].unique():
    tdf = plot_df[plot_df["Team"] == team]
    fig.add_trace(go.Scatter(
        x=tdf["Date"],
        y=tdf["SmoothedRating"],
        mode="lines",
        name=team,
        line=dict(color=team_colors.get(team, "grey"), width=2),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Rating: %{y:.2f}<br>"
            "Date: %{x|%b %d, %Y}<extra></extra>"
        ),
        text=[team] * len(tdf),
        showlegend=True
    ))

# === Custom dashed gridlines ===
GRID_COLOR = "#9e9e9e"  
bg_color = "lightgrey"

x_min = plot_df["Date"].min()
x_max = plot_df["Date"].max()
y_min = plot_df["SmoothedRating"].min()
y_max = plot_df["SmoothedRating"].max()

# pad slightly to avoid clipping
y_span = (y_max - y_min) if y_max > y_min else 1.0
y0, y1 = y_min - 0.05 * y_span, y_max + 0.05 * y_span

# Horizontal lines at every 0.5
start_half = floor(y0 * 2) / 2.0
end_half = ceil(y1 * 2) / 2.0
y_levels = np.arange(start_half, end_half + 0.0001, 0.5)

shapes = []
for y in y_levels:
    shapes.append(dict(
        type="line",
        x0=x_min, y0=y, x1=x_max, y1=y,
        line=dict(color=GRID_COLOR, width=1, dash="dash"),
        layer="below"
    ))

# Vertical lines at the 1st of each month within x range
first_month = datetime(x_min.year, x_min.month, 1)
if first_month < x_min:
    # advance to first of next month
    if first_month.month == 12:
        first_month = datetime(first_month.year + 1, 1, 1)
    else:
        first_month = datetime(first_month.year, first_month.month + 1, 1)

cursor = first_month
while cursor <= x_max:
    shapes.append(dict(
        type="line",
        x0=cursor, y0=y0, x1=cursor, y1=y1,
        line=dict(color=GRID_COLOR, width=1, dash="dash"),
        layer="below"
    ))
    # move to the first of the next month
    if cursor.month == 12:
        cursor = datetime(cursor.year + 1, 1, 1)
    else:
        cursor = datetime(cursor.year, cursor.month + 1, 1)

# === Axes & layout ===
fig.update_yaxes(
    title_text=None,
    showgrid=False,
    tick0=0,
    dtick=0.5
)
fig.update_xaxes(
    title_text=None,
    showgrid=False
)

fig.update_layout(
    title="Bookmaker-Derived Premier League Ratings 2024-2025",
    plot_bgcolor=bg_color,
    template="simple_white",
    hovermode="closest",
    legend=dict(title="Team", orientation="v", x=1.01, y=1),
    margin=dict(r=140),
    shapes=shapes
)

# === Save ===
os.makedirs("../viz", exist_ok=True)
fig.write_html(OUTPUT_HTML)
print(f"Interactive rolling ratings plot saved to {OUTPUT_HTML}")


