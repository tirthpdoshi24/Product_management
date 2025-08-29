# Run Project
# Install dependencies
pip install -r requirements.txt

# Run FastAPI
uvicorn predictor:app --host 0.0.0.0 --port 8000 --reload

# Create sqlite3 in memory tables
Run sqlite_db.py

# For api testing
Run api_testing.py