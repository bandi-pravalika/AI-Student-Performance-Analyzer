# AI Student Performance Analyzer 🎓

**Professional-grade ML system for predicting student performance with personalized recommendations.**

An enterprise-ready Machine Learning application with FastAPI backend and Streamlit frontend. Uses ensemble models, advanced feature engineering, and explainable AI to predict student performance and generate actionable recommendations.

## ✨ Key Features

### 🧠 ML Pipeline
- **Ensemble Models**: Random Forest (50%) + Gradient Boosting (30%) + Linear Regression (20%)
- **Feature Engineering**: Interaction terms, polynomial features, ratios, binned features
- **Advanced Preprocessing**: StandardScaler/MinMaxScaler, outlier removal, missing value handling
- **Comprehensive Metrics**: RMSE, MAE, R², prediction intervals, residual analysis

### 🔍 Explainability
- **SHAP-like Explanations**: Feature contributions to each prediction
- **Feature Importance**: Global importance scores from multiple models
- **Residual Analysis**: Detailed prediction error breakdown
- **Model Insights**: Automatic identification of patterns and anomalies

### 💼 Business Logic
- **Risk Assessment**: Multi-factor composite risk scoring
- **Intervention System**: Auto-detection of at-risk students
- **Smart Recommendations**: Context-aware, prioritized suggestions
- **Configurable Rules**: All thresholds customizable via environment variables

### 🏗️ Architecture
- **FastAPI Backend**: RESTful API with validation and error handling
- **Streamlit Frontend**: Rich interactive web UI with visualizations
- **Modular Design**: Clean separation of concerns across layers
- **Production Ready**: Comprehensive logging, configuration, error handling

## 📁 Project Structure

```
AI_Student_Performance_Analyzer/
├── src/
│   ├── core/               # Config, constants, exceptions
│   ├── data/              # Data generation, validation
│   ├── ml/
│   │   ├── models/        # ML model classes
│   │   ├── preprocessing/ # Scaling, outlier removal
│   │   ├── features/      # Feature engineering
│   │   ├── evaluation/    # Metrics and evaluation
│   │   └── explainability/# SHAP-like analysis
│   ├── business/          # Risk, recommendations
│   ├── api/              # FastAPI routes
│   ├── ui/               # Streamlit app
│   └── utils/            # Logging, helpers
├── tests/                # Unit tests
├── ml_models/v1/         # Model artifacts
├── main.py               # API entry point
├── train_model.py        # Training script
└── requirements.txt      # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Model (Optional)
```bash
python train_model.py
```

### 3. Start API Server
```bash
python -m uvicorn main:app --reload
```
API available at: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. Run Streamlit UI (New Terminal)
```bash
streamlit run src/ui/streamlit_app.py
```
UI available at: http://localhost:8501

## 📊 API Endpoints

### Health & Info
```
GET /api/v1/health              # Health check
GET /api/v1/info                # API information
```

### Predictions
```
POST /api/v1/predictions        # Single prediction
POST /api/v1/batch-predictions  # Multiple predictions
```

**Request Example:**
```json
{
  "Study_Hours": 5.0,
  "Attendance": 80.0,
  "Prev_Score": 75.0,
  "Test_Prep": 1
}
```

**Response Includes:**
- Predicted score and grade
- Risk assessment with confidence intervals
- Feature importance analysis
- SHAP-like explanations
- Personalized recommendations (with priorities)
- Intervention actions

### Model Info
```
GET /api/v1/models/info                 # Model details
GET /api/v1/models/feature-importance   # Feature importance
GET /api/v1/models/metrics              # Evaluation metrics
```

## ⚙️ Configuration

Create `.env` file in project root:

```bash
# API
DEBUG=False
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# ML
RANDOM_SEED=42
TEST_SIZE=0.2
FEATURE_SCALING=standard

# Thresholds
RISK_THRESHOLD_HIGH=55
RISK_THRESHOLD_MEDIUM=70
GRADE_A_MIN=85
GRADE_B_MIN=70
GRADE_C_MIN=55
STUDY_HOURS_THRESHOLD_LOW=4.0
STUDY_HOURS_THRESHOLD_HIGH=8.0
ATTENDANCE_THRESHOLD=75.0
PREV_SCORE_THRESHOLD=60.0
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/unit/ -v

# With coverage
pytest tests/unit/ --cov=src --cov-report=html
```

## 🎯 Model Architecture

### Ensemble Strategy
Weighted average of three complementary models:

| Model | Weight | Purpose |
|-------|--------|---------|
| Random Forest | 50% | Capture non-linear relationships |
| Gradient Boosting | 30% | Handle complex patterns |
| Linear Regression | 20% | Provide interpretability |

### Feature Set

**Base Features (4):**
- Study_Hours
- Attendance  
- Prev_Score
- Test_Prep

**Engineered Features (10):**
- Study_Hours × Prev_Score
- Attendance × Test_Prep
- Study_Hours × Test_Prep
- Study_Hours²
- Attendance²
- Prev_Score²
- Study_to_Attendance_Ratio
- PrevScore_to_Attendance
- Study_Level (categorical)
- Attendance_Level (categorical)

## 💡 Recommendations Engine

### Factors Analyzed
1. **Study Time**: < 4 hrs (needs increase) or > 8 hrs (needs balance)
2. **Attendance**: < 75% (improvement needed)
3. **Previous Score**: < 60% (revision recommended)
4. **Test Prep**: Completion status
5. **Predicted Score**: < 55% (urgent intervention)

### Output Format
Each recommendation includes:
- 🎯 Title and icon
- 📝 Detailed description
- 💡 Actionable suggestion
- 📈 Expected impact
- ✅ Specific action items
- 🔴 Priority level (urgent/high/medium/low)

## 📈 Example Usage

### Via API
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

result = response.json()
print(f"Predicted Score: {result['predicted_score']:.1f}")
print(f"Risk Level: {result['risk_level']}")
```

### Via Streamlit UI
1. Enter student details using sliders and inputs
2. Click "Predict Performance & Get Recommendations"
3. View comprehensive analysis with visualizations
4. Export results as JSON or CSV

## 🔧 Advanced Features

### SHAP-like Explanations
Shows how each feature contributes to the prediction:
```python
{
  "base_value": 70.0,
  "prediction": 78.5,
  "feature_values": {
    "Study_Hours": {
      "value": 5.0,
      "importance": 0.35,
      "contribution": 2.5
    },
    ...
  }
}
```

### Risk Assessment
Composite score combining:
- Predicted performance (40%)
- Attendance (30%)
- Study hours (20%)
- Previous performance (10%)

### Intervention System
Automatic triggers for:
- High risk (< 55 predicted score)
- Low attendance (< 75%)
- Low study hours (< 4)
- Previous performance issues (< 60%)

## 🛣️ Roadmap

### Phase 1: Foundation ✅
- [x] Refactor into modular architecture
- [x] Implement ensemble models
- [x] Add feature engineering
- [x] Build FastAPI backend
- [x] Create Streamlit UI

### Phase 2: Enhancement (Next)
- [ ] Add real student data
- [ ] Database integration (PostgreSQL)
- [ ] User authentication (JWT)
- [ ] Model versioning (MLflow)
- [ ] Advanced analytics dashboards

### Phase 3: Scale
- [ ] Mobile app (React Native)
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring (Prometheus/Grafana)
- [ ] LMS integrations (Canvas, Blackboard)

## 🔄 Improvements from Original

| Aspect | Original | Refactored |
|--------|----------|-----------|
| **Models** | 1 (Random Forest) | 3 ensemble (RF + GB + LR) |
| **Features** | 4 base | 14 engineered |
| **Preprocessing** | None | Scaling, outlier removal |
| **Evaluation** | Basic | Comprehensive metrics |
| **Explainability** | None | SHAP-like + feature importance |
| **Risk System** | Binary | Multi-factor scoring |
| **Architecture** | Monolith | Modular FastAPI + Streamlit |
| **Validation** | Minimal | Pydantic models |
| **Testing** | None | Unit test suite |
| **Logging** | None | Comprehensive logging |

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Add tests for new functionality
4. Submit pull request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check API docs at http://localhost:8000/docs
- Review logs in console output
