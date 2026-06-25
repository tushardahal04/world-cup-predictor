import pandas as pd


def predict(home_team, away_team, team_stats_df, model):

    home_team_stats = team_stats_df[team_stats_df["team"] == home_team].iloc[0]
    away_team_stats = team_stats_df[team_stats_df["team"] == away_team].iloc[0]

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
