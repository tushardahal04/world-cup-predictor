import pandas as pd

if __name__ == "__main__":
    results = pd.read_csv("data/raw/results.csv")
    # Only games between 2000 and 2026
    results["date"] = pd.to_datetime(results["date"], format="%Y-%m-%d")
    results = results[
        (results["date"].dt.year >= 2000) & (results["date"].dt.year < 2026)
    ]
    # Filter out friendlies
    results = results[results["tournament"] != "Friendly"]
    # Remove draws
    results = results[results["home_score"] != results["away_score"]]
    # Save new csv
    results.to_csv("data/processed/results_cleaned.csv", index=False)
    print(results.shape)
