# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, no authentication required. Future versions will include JWT-based authentication.

## Request/Response Format
- **Content-Type**: application/json
- **Encoding**: UTF-8

## Endpoints

### 1. Health Check
**GET** `/health`

Check API status.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "AI Student Performance Analyzer"
}
```

---

### 2. API Info
**GET** `/info`

Get API information and available endpoints.

**Response (200):**
```json
{
  "name": "AI Student Performance Analyzer API",
  "version": "1.0.0",
  "description": "ML-powered student performance prediction",
  "endpoints": {
    "predictions": "/api/v1/predictions",
    "models": "/api/v1/models",
    "health": "/api/v1/health"
  }
}
```

---

### 3. Single Prediction
**POST** `/predictions`

Predict student performance and get comprehensive analysis.

**Request Body:**
```json
{
  "Study_Hours": 5.0,
  "Attendance": 80.0,
  "Prev_Score": 75.0,
  "Test_Prep": 1
}
```

**Parameter Details:**
| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| Study_Hours | float | 0-15 | Weekly study hours |
| Attendance | float | 0-100 | Attendance percentage |
| Prev_Score | float | 0-100 | Previous exam score |
| Test_Prep | int | 0-1 | Test preparation completion (0=No, 1=Yes) |

**Response (200):**
```json
{
  "predicted_score": 78.5,
  "grade": "B",
  "risk_level": "Low",
  "risk_score": 25.3,
  "confidence_interval": {
    "lower": 72.1,
    "upper": 84.9,
    "margin": 6.4
  },
  "feature_importance": {
    "Study_Hours": 0.35,
    "Attendance": 0.28,
    "Prev_Score": 0.22,
    "Test_Prep": 0.15
  },
  "shap_explanation": {
    "base_value": 70.0,
    "prediction": 78.5,
    "output_value": 78.5,
    "feature_values": {
      "Study_Hours": {
        "value": 5.0,
        "importance": 0.35,
        "contribution": 2.975
      }
    }
  },
  "recommendations": [
    {
      "category": "study_time",
      "priority": "low",
      "icon": "✅",
      "title": "Study Schedule is Good",
      "description": "Your study hours (5.0/week) are in a healthy range.",
      "suggestion": "Maintain this consistent approach to studying.",
      "impact": "Consistent study habits lead to stable performance",
      "action_items": ["Continue with your current routine"]
    }
  ],
  "intervention_actions": []
}
```

**Error Responses:**

422 - Validation Error:
```json
{
  "detail": "Study_Hours must be between 0 and 15"
}
```

500 - Server Error:
```json
{
  "detail": "Prediction failed: [error message]"
}
```

---

### 4. Batch Predictions
**POST** `/batch-predictions`

Make predictions for multiple students.

**Request Body:**
```json
[
  {
    "Study_Hours": 5.0,
    "Attendance": 80.0,
    "Prev_Score": 75.0,
    "Test_Prep": 1
  },
  {
    "Study_Hours": 3.5,
    "Attendance": 70.0,
    "Prev_Score": 65.0,
    "Test_Prep": 0
  }
]
```

**Response (200):**
```json
{
  "predictions": [
    { /* prediction 1 */ },
    { /* prediction 2 */ }
  ]
}
```

---

### 5. Model Information
**GET** `/models/info`

Get information about trained models.

**Response (200):**
```json
{
  "ensemble_model": "Active",
  "weights": {
    "rf": 0.5,
    "gb": 0.3,
    "lr": 0.2
  },
  "components": {
    "rf": {
      "name": "RandomForest",
      "type": "RandomForestRegressor",
      "is_trained": true,
      "metrics": {
        "rmse": 3.45,
        "r2": 0.92,
        "mae": 2.15
      }
    },
    "gb": {
      "name": "GradientBoosting",
      "type": "GradientBoostingRegressor",
      "is_trained": true,
      "metrics": {
        "rmse": 3.12,
        "r2": 0.94,
        "mae": 1.98
      }
    },
    "lr": {
      "name": "LinearRegression",
      "type": "LinearRegression",
      "is_trained": true,
      "metrics": {
        "rmse": 5.23,
        "r2": 0.82,
        "mae": 4.21
      }
    }
  },
  "status": "Ready"
}
```

---

### 6. Feature Importance
**GET** `/models/feature-importance`

Get feature importance from all models.

**Response (200):**
```json
{
  "rf": {
    "Study_Hours": 0.35,
    "Attendance": 0.28,
    "Prev_Score": 0.22,
    "Test_Prep": 0.15
  },
  "gb": {
    "Study_Hours": 0.38,
    "Attendance": 0.26,
    "Prev_Score": 0.21,
    "Test_Prep": 0.15
  },
  "lr": {
    "Study_Hours": 0.32,
    "Attendance": 0.30,
    "Prev_Score": 0.25,
    "Test_Prep": 0.13
  }
}
```

---

### 7. Model Metrics
**GET** `/models/metrics`

Get evaluation metrics for all models.

**Response (200):**
```json
{
  "rf": {
    "rmse": 3.45,
    "r2": 0.92,
    "mae": 2.15
  },
  "gb": {
    "rmse": 3.12,
    "r2": 0.94,
    "mae": 1.98
  },
  "lr": {
    "rmse": 5.23,
    "r2": 0.82,
    "mae": 4.21
  }
}
```

---

## Error Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | OK | Successful request |
| 422 | Unprocessable Entity | Validation error in input |
| 500 | Internal Server Error | Server-side error |

## Rate Limiting

Currently, no rate limiting is implemented. Future versions may include:
- Per-IP rate limiting
- Per-API-key rate limiting
- Burst request handling

## Versioning

Current API version: **1.0.0**

API endpoints are versioned at `/api/v1/`. Future versions will be available at `/api/v2/`, etc.

## Response Times

**Typical response times:**
- Single prediction: 100-300ms
- Batch prediction (10 students): 500-1000ms
- Model info: 50-100ms

## Usage Examples

### Python
```python
import requests
import json

# Single prediction
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
print(f"Grade: {result['grade']}")
print(f"Risk Level: {result['risk_level']}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/predictions" \
  -H "Content-Type: application/json" \
  -d '{
    "Study_Hours": 5.0,
    "Attendance": 80.0,
    "Prev_Score": 75.0,
    "Test_Prep": 1
  }'
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/predictions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    Study_Hours: 5.0,
    Attendance: 80.0,
    Prev_Score: 75.0,
    Test_Prep: 1
  })
});

const result = await response.json();
console.log(`Predicted Score: ${result.predicted_score.toFixed(1)}`);
```

## Support

For API issues:
1. Check server status: `GET /api/v1/health`
2. Review interactive docs: `http://localhost:8000/docs`
3. Check console logs for error details
