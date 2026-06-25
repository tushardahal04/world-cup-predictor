import pandas as pd
import joblib
from features import get_team_stats
from datetime import datetime


def predict(home_team, away_team):
    model = joblib.load("model/model.pkl")
    results = pd.read_csv("data/processed/results_cleaned.csv")

    home_team_stats = get_team_stats(
        results, home_team, datetime.today().strftime("%Y-%m-%d")
    )
    away_team_stats = get_team_stats(
        results, away_team, datetime.today().strftime("%Y-%m-%d")
    )

    match_data = {
        "home_win_rate": home_team_stats["win_rate"],
        "home_avg_goals_scored": home_team_stats["avg_goals_scored"],
        "home_avg_goals_conceded": home_team_stats["avg_goals_conceded"],
        "away_win_rate": away_team_stats["win_rate"],
        "away_avg_goals_scored": away_team_stats["avg_goals_scored"],
        "away_avg_goals_conceded": away_team_stats["avg_goals_conceded"],
    }
    match_df = pd.DataFrame([match_data])

    prediction = model.predict(match_df)
    return prediction[0]


print(predict("England", "Brazil"))
print(predict("Brazil", "England"))
print(predict("France", "Germany"))
