
##########################################################
### Plot time series of all teams' ratings over season ###
##########################################################

import pandas as pd
import plotly.express as px
import os

# === CONFIG ===
INPUT_PATH = "../data/rolling_team_ratings.csv"
OUTPUT_HTML = "../viz/rolling_team_ratings.html"

# === Load data ===
df = pd.read_csv(INPUT_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# === Plot ===
fig = px.line(
    df,
    x="Date",
    y="Rating",
    color="Team",
    hover_name="Team",
    title="Premier League Rolling Team Ratings (3-game window)",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_layout(
    plot_bgcolor="lightgrey",
    hovermode="x unified",
    template="simple_white",
    legend=dict(title="Team", orientation="v", x=1.01, y=1),
    margin=dict(r=140)
)

# Optional: add logos as hover data if needed
# (Plotly only supports logos in scatter markers, not line traces)

# Save
os.makedirs("../viz", exist_ok=True)
fig.write_html(OUTPUT_HTML)
print(f"✅ Interactive rolling ratings plot saved to {OUTPUT_HTML}")

