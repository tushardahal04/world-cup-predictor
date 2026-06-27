import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def load_raw_data():
    return pd.read_csv("data/raw/results.csv")


results_df = load_raw_data()


def get_top_goals(df):
    # Total goals scored
    home_goals = df.groupby("home_team")["home_score"].sum()
    away_goals = df.groupby("away_team")["away_score"].sum()
    total_goals = (home_goals + away_goals).sort_values(ascending=False)
    return total_goals.head(10)


def get_win_rates(df):
    # Get home and away wins
    home_wins = df[df["home_score"] > df["away_score"]].groupby("home_team").size()
    away_wins = df[df["away_score"] > df["home_score"]].groupby("away_team").size()
    home_games = df.groupby("home_team").size()
    away_games = df.groupby("away_team").size()
    total_games = home_games + away_games
    # Minimum 100 games played
    total_win_rate = (home_wins + away_wins) / total_games
    total_win_rate = total_win_rate[total_games >= 100]
    return total_win_rate.sort_values(ascending=False).head(10)


def goals_scored_per_year(df):
    # Convert dates and groupby
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["total_goals"] = df["home_score"] + df["away_score"]
    total_goals = df.groupby(df["date"].dt.year)["total_goals"].sum()
    return total_goals


def home_vs_draws_vs_away(df):
    # Get percentage of games that were home and away wins
    home_wins = df[df["home_score"] > df["away_score"]].shape[0]
    away_wins = df[df["away_score"] > df["home_score"]].shape[0]
    draws = df[df["home_score"] == df["away_score"]].shape[0]
    return pd.Series({"Home wins": home_wins, "Away wins": away_wins, "Draws": draws})


st.set_page_config(page_title="World Cup Prediction Engine")
st.title("International Analytics")

# Total goals chart
total_goals_data = get_top_goals(results_df)
total_goals_chart = px.bar(
    total_goals_data,
    x=total_goals_data.index,
    y=total_goals_data.values,
    labels={"x": "Team", "y": "Goals scored"},
    title="Top 10 goal scoring nations",
)
# Top win rates (min 100 games)
total_win_rates_data = get_win_rates(results_df)
total_win_rates_chart = px.bar(
    total_win_rates_data,
    x=total_win_rates_data.index,
    y=total_win_rates_data.values,
    labels={"x": "Team", "y": "Win rate %"},
    title="Top 10 highest win rate nations (min 100 games)",
)
# Total goals scored per year
total_goals_scored_per_year_data = goals_scored_per_year(results_df)
total_goals_scored_per_year_chart = px.bar(
    total_goals_scored_per_year_data,
    x=total_goals_scored_per_year_data.index,
    y=total_goals_scored_per_year_data.values,
    labels={"x": "Year", "y": "Total goals scored"},
    title="Total goals scored per year",
)
# Home vs away vs draws
home_vs_draws_vs_away_data = home_vs_draws_vs_away(results_df)
home_vs_draws_vs_away_chart = px.pie(
    values=home_vs_draws_vs_away_data.values,
    names=home_vs_draws_vs_away_data.index,
    title="Home wins vs Draws vs Away wins",
)

st.plotly_chart(total_goals_chart)
st.plotly_chart(total_win_rates_chart)
st.plotly_chart(total_goals_scored_per_year_chart)
st.plotly_chart(home_vs_draws_vs_away_chart)
