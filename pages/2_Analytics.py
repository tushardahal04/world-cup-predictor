import streamlit as st
import pandas as pd


@st.cache_data
def get_top_goals():
    results_df = pd.read_csv("data/raw/results.csv")
    # Total goals scored
    home_goals = results_df.groupby("home_team")["home_score"].sum()
    away_goals = results_df.groupby("away_team")["away_score"].sum()
    total_goals = (home_goals + away_goals).sort_values(ascending=False)
    print(total_goals)
    return total_goals.head(10)


st.set_page_config(page_title="Analytics")
st.title("Analytics")

top_goals = st.bar_chart(get_top_goals())
