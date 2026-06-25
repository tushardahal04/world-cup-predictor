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
        "average_goals_conceded": average_goals_conceded,
    }


print(get_team_stats(results, "Brazil", "2026-06-24"))
