# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### Step 2: Start FastAPI Backend (Terminal 1)
```bash
python -m uvicorn main:app --reload
```
✅ API running at: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Step 3: Start Streamlit UI (Terminal 2)
```bash
streamlit run src/ui/streamlit_app.py
```
✅ App running at: http://localhost:8501

### Step 4: Make a Prediction
In the Streamlit app:
1. Use the sliders to enter student details:
   - Study Hours: 5.0
   - Attendance: 80%
   - Previous Score: 75
   - Test Prep: Yes
2. Click "🔮 Predict Performance"
3. View predictions, recommendations, and analysis!

---

## 🧪 Quick Testing

### Test via Streamlit UI
The UI is the easiest way to test all features with visualizations.

### Test via API (Python)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/predictions",
    json={
        "Study_Hours": 5.0,
        "Attendance": 80.0,
        "Prev_Score": 75.0,
        "Test_Prep": 1
    }
)

print(response.json())
```

### Test via API (cURL)
```bash
curl -X POST "http://localhost:8000/api/v1/predictions" \
  -H "Content-Type: application/json" \
  -d '{"Study_Hours": 5.0, "Attendance": 80.0, "Prev_Score": 75.0, "Test_Prep": 1}'
```

### Run Unit Tests
```bash
pytest tests/unit/ -v
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Start the API server |
| `src/ui/streamlit_app.py` | Run the web UI |
| `train_model.py` | Train/update models |
| `src/core/config.py` | Configuration settings |
| `docs/API.md` | Full API documentation |
| `docs/ML_MODELS.md` | ML model details |

---

## ⚙️ Configuration

Optional: Create `.env` file to customize settings:
```bash
DEBUG=False
LOG_LEVEL=INFO
API_PORT=8000

# Thresholds
GRADE_A_MIN=85
RISK_THRESHOLD_HIGH=55
STUDY_HOURS_THRESHOLD_LOW=4.0
ATTENDANCE_THRESHOLD=75.0
PREV_SCORE_THRESHOLD=60.0
```

---

## 🎯 What You Get

### Predictions
- Predicted exam score (0-100)
- Grade (A/B/C/F)
- Risk level (Low/Medium/High)
- Confidence intervals (±margin)

### Analysis
- Feature importance (what matters most)
- SHAP-like explanations (why this prediction)
- Risk indicators (what's risky)
- Residual analysis (prediction accuracy)

### Recommendations
- Personalized suggestions
- Action items per recommendation
- Priority levels (urgent → low)
- Expected impact statements

### Interventions
- At-risk student identification
- Automated intervention triggers
- Suggested actions for teachers/counselors

---

## 💡 Example Scenarios

### Scenario 1: High-Performing Student
- Study Hours: 6.0
- Attendance: 90%
- Prev Score: 85
- Test Prep: Yes

**Expected Result:**
- High predicted score (~87)
- Low risk level
- Recommendations: Maintain current habits
- No intervention needed

### Scenario 2: At-Risk Student
- Study Hours: 2.5
- Attendance: 65%
- Prev Score: 55
- Test Prep: No

**Expected Result:**
- Low predicted score (~48)
- High risk level (urgent)
- Recommendations: Increase study hours, attend more classes, get tutoring
- Intervention: Urgent teacher meeting needed

### Scenario 3: Average Student
- Study Hours: 4.0
- Attendance: 75%
- Prev Score: 70
- Test Prep: No

**Expected Result:**
- Medium predicted score (~72)
- Medium risk level
- Recommendations: Mixed (some areas good, some need work)
- Intervention: Monitor progress

---

## 🔧 Troubleshooting

### API not starting?
```bash
# Check if port 8000 is in use
# Try a different port:
python -m uvicorn main:app --reload --port 8001
```

### Streamlit connection error?
```bash
# Make sure API is running first
# Check API is at http://localhost:8000/health
```

### Import errors?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Tests failing?
```bash
# Run with verbose output
pytest tests/unit/ -v -s
```

---

## 📈 Next Steps

### Immediate
- Explore predictions for different scenarios
- Try API endpoints directly
- Read documentation (README.md, API.md)
- Run unit tests to verify functionality

### Short Term
- Train model with more/real data: `python train_model.py`
- Customize thresholds via `.env` file
- Modify recommendations rules in `src/business/recommendations.py`

### Medium Term
- Connect to real student database
- Add authentication (JWT)
- Deploy with Docker
- Add monitoring/logging

### Long Term
- Try new ML models (XGBoost, neural nets)
- Implement LMS integrations
- Build mobile app
- Deploy to production infrastructure

---

## 📚 Documentation

**Read These:**
1. `README.md` - Project overview
2. `REFACTORING_SUMMARY.md` - What changed
3. `docs/API.md` - API endpoints
4. `docs/ML_MODELS.md` - Model details

---

## ✅ Verification Checklist

After starting the system, verify:

- [ ] API server starts without errors
- [ ] API docs page loads: http://localhost:8000/docs
- [ ] Health check passes: http://localhost:8000/api/v1/health
- [ ] Streamlit app starts without errors
- [ ] Can enter values and get predictions
- [ ] Predictions show recommendations
- [ ] Export buttons work
- [ ] Unit tests pass: `pytest tests/unit/ -v`

---

## 🎉 You're Ready!

Everything is set up and ready to use. Start the API and UI, try making predictions, and explore the features.

For more details, see the documentation files in the `docs/` directory.

Happy analyzing! 🎓
