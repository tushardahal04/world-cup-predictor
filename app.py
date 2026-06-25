import pandas as pd
import streamlit as st

from src.predict import predict

results = pd.read_csv("data/processed/results_cleaned.csv")
home_teams = results["home_team"]
away_teams = results["away_team"]

teams = sorted(pd.concat([home_teams, away_teams]).unique().tolist())

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
    prediction = predict(home_team, away_team)
    if prediction == "home":
        st.write(str(home_team) + " wins!")
    elif prediction == "away":
        st.write(str(away_team) + " wins!")
    else:
        st.write("It's a draw!")
