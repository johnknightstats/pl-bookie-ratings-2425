# Premier League Bookmaker Ratings (2024–25)

This repo estimates **rolling strength ratings** for Premier League teams using **Pinnacle Sports Asian handicap lines** (via the excellent [Football-Data](https://www.football-data.co.uk/)). Ratings are computed per match date from the market’s view (line + odds), not from goals scored.

**Why markets?** Sharp books aggregate informed money. Converting their closing handicap + odds into an expected goal difference produces a robust, model‑light rating signal.

## Method (concise)

- For each match, take the **Asian handicap line** (AHh) and learn an **odds-based adjustment** from Pinnacle’s closing home odds (PCAHH):
  - Regress **(GoalDiff − AHh)** on **PCAHH** to map odds → goal adjustment.
  - Predicted handicap = **AHh + Adjustment** (= “Handicap_Pred”).
- For each **match date**:
  - Teams **playing** that day use **prev/current/next** fixtures (3).
  - Teams **not playing** use **prev/next** fixtures (2).
  - Fit ratings to minimize squared error between **(home − away + H)** and **Handicap_Pred**, where **H** is a **single, season‑wide** home advantage (the mean of Handicap_Pred).
  - Do **not** compute ratings for the final match date (but use it as “+1” for the penultimate window).
  - Center ratings to mean 0; higher = stronger team.
- Plot a time series (optional **LOESS smoothing**, default `frac=0.2`) with team colors and custom gridlines.

## Repo Structure

pl-bookie-ratings-2425/
├── data/
│ ├── E0_raw.csv
│ ├── E0_clean.csv
│ ├── E0_with_handicap.csv
│ └── rolling_team_ratings.csv
├── scripts/
│ ├── download_data.py
│ ├── preprocess_data.py
│ ├── regression_handicap.py
│ ├── rolling_optimize_ratings.py
│ ├── plot_rolling_ratings.py
│ └── run_pipeline.py
├── viz/
│ ├── team_ratings_rolling.png
│ └── rolling_team_ratings.html
├── logos/ # (optional) team badges for hover/legend UX
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

## Quickstart

1) Install deps
pip install -r requirements.txt

2) Run the end-to-end pipeline from the repo root
python scripts/run_pipeline.py

Outputs:
- data/E0_* CSVs (raw → clean → with handicaps)
- data/rolling_team_ratings.csv (per-date ratings)
- viz/rolling_team_ratings.html (interactive)
- viz/team_ratings_rolling.png (static preview)


## Data Source & Attribution

- Match data & Pinnacle closing lines: Football-Data

- Please review their terms of use. This repo ingests CSVs from their archive for research/visualisation.

## Disclaimer

This project is for research and educational purposes. It does not constitute betting advice.

## License

This project is released under the MIT License (see LICENSE).