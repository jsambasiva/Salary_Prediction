"""Train, save and load the salary prediction model.

The model is trained on synthetic data so the project runs out of the box.
To use real data, replace `generate_data()` with `pd.read_csv("your_data.csv")`
(keep the same column names).
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_PATH = Path(__file__).parent / "salary_model.joblib"

NUMERIC = ["experience"]
CATEGORICAL = ["education", "job_role", "city_tier"]

# Base annual salary (INR, in lakhs) for a bachelor's graduate with 0 years of experience.
ROLE_BASE = {
    "Software Engineer": 8.0,
    "Data Scientist": 9.0,
    "Data Analyst": 5.5,
    "Web Developer": 6.0,
    "DevOps Engineer": 8.5,
    "UI/UX Designer": 6.0,
}
EDU_FACTOR = {"High School": 0.7, "Bachelor": 1.0, "Master": 1.2, "PhD": 1.4}
CITY_FACTOR = {"Tier 1": 1.2, "Tier 2": 1.0, "Tier 3": 0.85}


def generate_data(n: int = 4000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "experience": rng.uniform(0, 25, n).round(1),
            "education": rng.choice(list(EDU_FACTOR), n),
            "job_role": rng.choice(list(ROLE_BASE), n),
            "city_tier": rng.choice(list(CITY_FACTOR), n),
        }
    )
    lakhs = (
        df["job_role"].map(ROLE_BASE)
        * df["education"].map(EDU_FACTOR)
        * df["city_tier"].map(CITY_FACTOR)
        * (1 + 0.12 * df["experience"])
        * rng.normal(1, 0.06, n)
    )
    df["salary"] = (lakhs * 100_000).round(0)
    return df


def train_model() -> Pipeline:
    df = generate_data()
    X, y = df[NUMERIC + CATEGORICAL], df["salary"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    pipeline = Pipeline(
        [
            (
                "prep",
                ColumnTransformer(
                    [("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL)],
                    remainder="passthrough",
                ),
            ),
            ("model", RandomForestRegressor(n_estimators=200, random_state=1, n_jobs=-1)),
        ]
    )
    pipeline.fit(X_train, y_train)
    print(f"Model trained. R-squared on test data: {r2_score(y_test, pipeline.predict(X_test)):.3f}")
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline


def load_model() -> Pipeline:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train_model()


if __name__ == "__main__":
    train_model()

