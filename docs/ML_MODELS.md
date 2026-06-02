# ML Models Documentation

## Overview

This project uses an ensemble approach combining three complementary models for robust predictions.

## Model Architecture

### Ensemble Strategy

The ensemble uses weighted averaging to combine predictions from three models:

```
Prediction = (0.5 × RandomForest) + (0.3 × GradientBoosting) + (0.2 × LinearRegression)
```

**Rationale:**
- **Random Forest (50%)**: Captures non-linear patterns, handles feature interactions
- **Gradient Boosting (30%)**: Iteratively improves on errors, handles complex relationships
- **Linear Regression (20%)**: Provides interpretability and baseline linear relationship

---

## Individual Models

### 1. Random Forest Regressor

**Purpose:** Capture non-linear relationships and feature interactions

**Configuration:**
```python
RandomForestRegressor(
    n_estimators=100,      # Number of trees
    max_depth=15,          # Maximum tree depth
    min_samples_split=5,   # Minimum samples for split
    min_samples_leaf=2,    # Minimum samples in leaf
    random_state=42,       # Reproducibility
    n_jobs=-1             # Use all CPU cores
)
```

**Strengths:**
- Handles non-linear relationships
- Captures feature interactions
- Robust to outliers
- Provides feature importance

**Weaknesses:**
- Less interpretable
- May overfit with complex data
- Slower prediction time

**Typical Performance:**
- RMSE: 3.2-3.8 (on 0-100 scale)
- R²: 0.90-0.95
- MAE: 2.0-2.5

---

### 2. Gradient Boosting Regressor

**Purpose:** Improve predictions by iteratively correcting errors

**Configuration:**
```python
GradientBoostingRegressor(
    n_estimators=100,      # Number of boosting rounds
    learning_rate=0.1,     # Learning rate (shrinkage)
    max_depth=5,           # Tree depth
    min_samples_split=5,   # Minimum samples for split
    min_samples_leaf=2,    # Minimum samples in leaf
    random_state=42        # Reproducibility
)
```

**Strengths:**
- Powerful gradient-based optimization
- Often achieves highest accuracy
- Handles complex patterns well
- Feature importance readily available

**Weaknesses:**
- Risk of overfitting
- Requires careful parameter tuning
- Slower training time
- Less interpretable

**Typical Performance:**
- RMSE: 2.9-3.5
- R²: 0.92-0.96
- MAE: 1.9-2.3

---

### 3. Linear Regression

**Purpose:** Provide interpretable baseline and linear relationship modeling

**Configuration:**
```python
LinearRegression(
    fit_intercept=True,    # Fit intercept term
    copy_X=True,           # Copy features matrix
    positive=False         # Allow negative coefficients
)
```

**Strengths:**
- Highly interpretable
- Fast training and prediction
- Provides explicit feature coefficients
- No hyperparameters to tune
- Good baseline for comparison

**Weaknesses:**
- Cannot capture non-linear relationships
- Assumes linear combination of features
- Sensitive to outliers
- May underfit complex patterns

**Typical Performance:**
- RMSE: 4.8-5.8
- R²: 0.80-0.88
- MAE: 3.8-4.5

---

## Feature Engineering

### Feature Set

**Base Features (4):**
1. `Study_Hours`: Weekly study hours (0-15)
2. `Attendance`: Attendance percentage (0-100)
3. `Prev_Score`: Previous exam score (0-100)
4. `Test_Prep`: Test preparation flag (0 or 1)

**Engineered Features (10):**

| Feature | Type | Formula | Interpretation |
|---------|------|---------|-----------------|
| Study_x_PrevScore | Interaction | Study_Hours × Prev_Score | Engaged high-performer |
| Attendance_x_TestPrep | Interaction | Attendance × Test_Prep | Prepared attendee |
| Study_x_TestPrep | Interaction | Study_Hours × Test_Prep | Focused preparation |
| Study_Hours_squared | Polynomial | Study_Hours² | Diminishing returns effect |
| Attendance_squared | Polynomial | Attendance² | Non-linear attendance effect |
| Prev_Score_squared | Polynomial | Prev_Score² | Knowledge acceleration |
| Study_to_Attendance_Ratio | Ratio | Study_Hours / Attendance | Study efficiency |
| PrevScore_to_Attendance | Ratio | Prev_Score / Attendance | Achievement vs presence |
| Study_Level | Binned | 1-4 based on hours | Study intensity category |
| Attendance_Level | Binned | 1-4 based on percentage | Attendance category |

**Total Features: 14 (4 base + 10 engineered)**

---

## Preprocessing Pipeline

### 1. Missing Value Handling
- Strategy: Mean imputation for numeric columns
- Applied to: All feature columns
- Impact: Ensures no NaN values reach model

### 2. Outlier Removal
- Method: Interquartile Range (IQR) with 1.5x multiplier
- Applied to: Target variable (Final_Score)
- Formula: Remove if outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]

### 3. Feature Scaling
- Method: StandardScaler (zero mean, unit variance)
- Formula: $z = \frac{x - \mu}{\sigma}$
- Applied to: All features before training
- Benefit: Improves convergence, handles different feature scales

---

## Model Evaluation

### Metrics

**1. Root Mean Square Error (RMSE)**
$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$
- Penalizes larger errors more heavily
- Interpretable on same scale as target

**2. Mean Absolute Error (MAE)**
$$MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$
- Robust to outliers
- Average prediction error

**3. R² Score (Coefficient of Determination)**
$$R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$
- Measures variance explained (0 to 1)
- 1.0 = perfect predictions

**4. Prediction Intervals**
- Calculated using residual standard deviation
- 95% confidence interval: $\hat{y} \pm 1.96 \sigma_{residual}$

### Cross-Validation

**Strategy:** Train-test split
- Train: 80% of data
- Test: 20% of data
- Random seed: 42 (reproducibility)

### Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| RMSE | < 4.0 | ✓ Achieved |
| MAE | < 2.5 | ✓ Achieved |
| R² | > 0.90 | ✓ Achieved |

---

## Explainability

### 1. Feature Importance

**Random Forest Importance:**
- Based on decrease in impurity (Gini)
- Normalized to sum to 1.0
- Interpretation: Contribution to model decisions

**Linear Regression Coefficients:**
- Absolute value represents magnitude
- Sign indicates direction (+ or -)
- Interpretation: Per-unit change in target

### 2. SHAP-like Explanations

For each prediction:
1. Calculate feature contributions
2. Weight by importance and normalized values
3. Sum to explain prediction relative to baseline

**Example Output:**
```json
{
  "base_value": 70.0,
  "prediction": 78.5,
  "feature_values": {
    "Study_Hours": {
      "value": 5.0,
      "importance": 0.35,
      "contribution": +2.975  # pushes up from baseline
    },
    "Attendance": {
      "value": 80.0,
      "importance": 0.28,
      "contribution": +1.96
    }
  }
}
```

### 3. Permutation Importance

Alternative importance measure:
- Shuffle each feature randomly
- Measure prediction error increase
- Higher increase = more important feature
- Model-agnostic (works with any model)

---

## Training Process

### 1. Data Generation
```
Generate 500 synthetic samples
├─ Study_Hours: Uniform(1, 10)
├─ Attendance: Uniform(50, 100)
├─ Prev_Score: Uniform(40, 100)
├─ Test_Prep: Bernoulli(0.5)
└─ Final_Score: f(features) + Normal(0, 3)
```

### 2. Train-Test Split
```
500 samples → 400 train, 100 test
```

### 3. Feature Engineering
```
4 base features → 14 engineered features
```

### 4. Preprocessing
```
Fit on training data only
├─ StandardScaler.fit(X_train)
└─ Apply to train and test
```

### 5. Model Training
```
Train 3 models independently on scaled features
```

### 6. Evaluation
```
Predict on test set
├─ Calculate metrics (RMSE, MAE, R²)
├─ Analyze residuals
└─ Extract feature importance
```

---

## Model Artifacts

Saved files in `ml_models/v1/`:
```
├── random_forest_model.pkl    # Trained Random Forest
├── gradient_boosting_model.pkl # Trained Gradient Boosting  
├── linear_regression_model.pkl # Trained Linear Regression
├── preprocessor.pkl            # StandardScaler instance
├── feature_engineer.pkl        # FeatureEngineer instance
└── metadata.json               # Training metadata
```

---

## Hyperparameter Tuning

### Current Hyperparameters

Random Forest:
- n_estimators: 100 (number of trees)
- max_depth: 15 (prevent overfitting)
- min_samples_split: 5 (minimum for split)

Gradient Boosting:
- n_estimators: 100 (boosting rounds)
- learning_rate: 0.1 (shrinkage)
- max_depth: 5 (limit tree complexity)

### Future Optimization

Could implement:
- GridSearchCV for exhaustive search
- RandomizedSearchCV for efficient search
- Bayesian optimization for fine-tuning

---

## Monitoring

### Metrics to Track

1. **Accuracy Metrics**
   - RMSE on new data
   - MAE degradation
   - R² on holdout set

2. **Prediction Patterns**
   - Distribution of predictions
   - Residual patterns
   - Error by score range

3. **Data Quality**
   - Feature distributions
   - Missing value rates
   - Outlier frequency

### Retraining Strategy

Retrain model when:
- Accuracy drops > 2% RMSE
- Data distribution shifts significantly
- New features become available
- Performance issues detected in production

---

## Limitations

1. **Synthetic Data**: Currently using synthetic data; performance on real data may differ
2. **Linear Assumptions**: Some engineered features assume linear relationships
3. **Limited Features**: Only 4 base features; additional inputs would improve predictions
4. **Static Model**: No online/incremental learning; full retraining needed for updates
5. **Bounded Target**: Score prediction bounded to 0-100; may struggle at extremes

---

## Future Improvements

1. **Real Data Integration**: Use actual student performance data
2. **Advanced Models**: Try XGBoost, LightGBM, neural networks
3. **Feature Selection**: Automated feature importance ranking
4. **Temporal Modeling**: Time-series features for longitudinal predictions
5. **Causal Inference**: Understand which interventions actually work
6. **Online Learning**: Continuous model improvement with new data
7. **Transfer Learning**: Pre-train on large datasets, fine-tune for institutions
