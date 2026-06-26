import pandas as pd

results = pd.read_csv("data/processed/results_cleaned.csv")


# Returns all matches from a team before a specified date from the data frame
def get_team_matches(df, team, date):
    return df[
        ((df["home_team"] == team) | (df["away_team"] == team)) & (df["date"] < date)
    ]


# Returns win rate, average goals scored and conceced for the last n games
def get_team_stats(df, team, date, n=10):
    team_matches = get_team_matches(df, team, date).tail(n)

    # Win rate
    home_wins_df = team_matches[
        (team_matches["home_team"] == team)
        & (team_matches["home_score"] > team_matches["away_score"])
    ]
    away_wins_df = team_matches[
        (team_matches["away_team"] == team)
        & (team_matches["away_score"] > team_matches["home_score"])
    ]
    home_wins = home_wins_df.shape[0]
    away_wins = away_wins_df.shape[0]
    win_rate = (home_wins + away_wins) / n

    # Average goals scored
    home_goals_scored = team_matches[team_matches["home_team"] == team][
        "home_score"
    ].sum()
    away_goals_scored = team_matches[team_matches["away_team"] == team][
        "away_score"
    ].sum()
    average_goals_scored = (home_goals_scored + away_goals_scored) / n

    # Average goals conceced
    home_goals_conceded = team_matches[team_matches["home_team"] == team][
        "away_score"
    ].sum()
    away_goals_conceded = team_matches[team_matches["away_team"] == team][
        "home_score"
    ].sum()
    average_goals_conceded = (home_goals_conceded + away_goals_conceded) / n

    return {
        "win_rate": win_rate,
        "avg_goals_scored": average_goals_scored,
        "avg_goals_conceded": average_goals_conceded,
    }


def build_features(df):
    rows_list = []
    for index, rows in df.iterrows():
        result = ""
        home_team_stats = get_team_stats(df, rows["home_team"], rows["date"])
        away_team_stats = get_team_stats(df, rows["away_team"], rows["date"])

        # Check which team won
        if rows["home_score"] == rows["away_score"]:
            result = "draw"
        elif rows["home_score"] > rows["away_score"]:
            result = "home"
        else:
            result = "away"

        # Make dict
        row_data = {
            "home_win_rate": home_team_stats["win_rate"],
            "home_avg_goals_scored": home_team_stats["avg_goals_scored"],
            "home_avg_goals_conceded": home_team_stats["avg_goals_conceded"],
            "away_win_rate": away_team_stats["win_rate"],
            "away_avg_goals_scored": away_team_stats["avg_goals_scored"],
            "away_avg_goals_conceded": away_team_stats["avg_goals_conceded"],
            "result": result,
        }

        rows_list.append(row_data)
    return pd.DataFrame(rows_list)


if __name__ == "__main__":
    features_df = build_features(results)
    features_df.to_csv("data/processed/features.csv", index=False)
