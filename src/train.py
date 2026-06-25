from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

features_df = pd.read_csv("data/processed/features.csv")

X = features_df.drop("result", axis=1)
y = features_df["result"]
# 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Baseline model, to be tuned
model = RandomForestClassifier()
model.fit(X_train, y_train)

rating = model.score(X_test, y_test)
_ = joblib.dump(model, "model/model.pkl")
