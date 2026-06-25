from datetime import datetime
import pandas as pd
from features import get_team_stats

if __name__ == "__main__":
    df = pd.read_csv("data/processed/results_cleaned.csv")

    home_teams = df["home_team"]
    away_teams = df["away_team"]
    teams = sorted(pd.concat([home_teams, away_teams]).unique().tolist())

    rows_list = []
    for team in teams:
        team_stats = get_team_stats(df, team, datetime.today().strftime("%Y-%m-%d"))
        team_stats["team"] = team
        rows_list.append(team_stats)

    df = pd.DataFrame(rows_list)
    df.to_csv("data/processed/team_stats.csv", index=False)
