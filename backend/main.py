"""FastAPI app: serves the prediction API and the static frontend.

Run from the `backend` folder:  uvicorn main:app --reload
"""
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from model import load_model
from schemas import SalaryRequest, SalaryResponse

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Salary Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()


@app.get("/api/health")
@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.post("/api/predict", response_model=SalaryResponse)
def predict(data: SalaryRequest):
    row = pd.DataFrame([data.model_dump()])
    prediction = float(model.predict(row)[0])

    # Spread of the individual trees gives a simple confidence range.
    forest = model.named_steps["model"]
    X = model.named_steps["prep"].transform(row)
    tree_preds = np.array([t.predict(X)[0] for t in forest.estimators_])
    low, high = np.percentile(tree_preds, [10, 90])

    return SalaryResponse(
        predicted_salary=round(prediction),
        lower_estimate=round(float(low)),
        upper_estimate=round(float(high)),
    )


# ---- Frontend ---------------------------------------------------------------
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


