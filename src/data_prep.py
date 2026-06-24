import pandas as pd

results = pd.read_csv("data/raw/results.csv")
# Filter out 2026 games
results["date"] = pd.to_datetime(results["date"], format="%Y-%m-%d")
results = results[results["date"].dt.year < 2026]

print(results)
