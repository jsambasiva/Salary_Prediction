# Salary Prediction

A small full-stack app with an HTML/CSS/JavaScript frontend and a FastAPI backend using a scikit-learn model.

## Project structure

```text
frontend/
  index.html
  style.css
  script.js
backend/
  main.py
  model.py
  schemas.py
  requirements.txt
  requirements-full.txt  # full environment snapshot (optional)
README.md
.gitignore
```

## Run

From the project root, create and activate a virtual environment, then install the backend dependencies:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
```

Start the API from the backend directory:

```bash
cd backend
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 (API docs: http://127.0.0.1:8000/docs). The model trains on first start and is saved as `backend/salary_model.joblib`.

## API

`POST /api/predict`

```json
{ "experience": 3, "education": "Bachelor", "job_role": "Data Scientist", "city_tier": "Tier 2" }
```
