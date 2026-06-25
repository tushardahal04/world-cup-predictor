import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

features_df = pd.read_csv("data/processed/features.csv")

X = features_df.drop("result", axis=1)
y = features_df["result"]
# 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Baseline model, to be tuned
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

rating = model.score(X_test, y_test)
print(rating)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

_ = joblib.dump(model, "model/model.pkl")
