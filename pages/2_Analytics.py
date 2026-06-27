import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_top_goals():
    results_df = pd.read_csv("data/raw/results.csv")
    # Total goals scored
    home_goals = results_df.groupby("home_team")["home_score"].sum()
    away_goals = results_df.groupby("away_team")["away_score"].sum()
    total_goals = (home_goals + away_goals).sort_values(ascending=False)
    return total_goals.head(10)


@st.cache_data
def get_win_rates():
    results_df = pd.read_csv("data/raw/results.csv")
    # Get home and away wins
    home_wins = (
        results_df[results_df["home_score"] > results_df["away_score"]]
        .groupby("home_team")
        .size()
    )
    away_wins = (
        results_df[results_df["away_score"] > results_df["home_score"]]
        .groupby("away_team")
        .size()
    )
    home_games = results_df.groupby("home_team").size()
    away_games = results_df.groupby("away_team").size()
    total_games = home_games + away_games
    # Minimum 100 games played
    total_win_rate = (home_wins + away_wins) / total_games
    total_win_rate = total_win_rate[total_games >= 100]
    return total_win_rate.sort_values(ascending=False).head(10)


st.set_page_config(page_title="Analytics")
st.title("Analytics")
get_win_rates()

total_goals_data = get_top_goals()
total_goals_chart = px.bar(
    total_goals_data,
    x=total_goals_data.index,
    y=total_goals_data.values,
    labels={"x": "Team", "y": "Goals scored"},
    title="Top 10 goal scoring nations",
)

total_win_rates_data = get_win_rates()
total_win_rates_chart = px.bar(
    total_win_rates_data,
    x=total_win_rates_data.index,
    y=total_win_rates_data.values,
    labels={"x": "Team", "y": "Win rate %"},
    title="Top 10 highest win rate nations",
)

st.plotly_chart(total_goals_chart)
st.plotly_chart(total_win_rates_chart)
