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


print(get_team_stats(results, "Brazil", "2026-06-24"))
