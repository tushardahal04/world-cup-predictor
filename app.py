import joblib
import pandas as pd
import streamlit as st
from src.predict import predict


@st.cache_data
def load_data():
    return pd.read_csv("data/processed/team_stats.csv")


@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")


team_stats_df = load_data()
model = load_model()
teams = sorted(team_stats_df["team"].unique().tolist())

st.title("World Cup Prediction Engine")
home_col, away_col = st.columns(2)
with home_col:
    home_team = st.selectbox(
        "Home Team", teams, index=None, placeholder="Select home team"
    )
with away_col:
    away_team = st.selectbox(
        "Away Team", teams, index=None, placeholder="Select away team"
    )
if st.button("Confirm"):
    prediction = predict(home_team, away_team, team_stats_df, model)
    if prediction == "home":
        st.write(str(home_team) + " wins!")
    elif prediction == "away":
        st.write(str(away_team) + " wins!")
    else:
        st.write("It's a draw!")
