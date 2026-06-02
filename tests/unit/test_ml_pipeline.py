"""Unit tests for ML pipeline."""
import pytest
import pandas as pd
import numpy as np
from src.data.generator import generate_synthetic_data, validate_input_data
from src.ml.models.model import RandomForestModel, GradientBoostingModel, EnsembleModel
from src.ml.preprocessing.pipeline import PreprocessingPipeline
from src.ml.features.engineer import FeatureEngineer
from src.ml.evaluation.metrics import ModelEvaluator
from src.business.risk import RiskAssessment
from src.business.recommendations import RecommendationEngine
from src.core.exceptions import DataValidationError


class TestDataGeneration:
    """Test data generation module."""
    
    def test_generate_synthetic_data(self):
        """Test synthetic data generation."""
        df = generate_synthetic_data(n_samples=100)
        assert len(df) == 100
        assert 'Final_Score' in df.columns
        assert df['Final_Score'].min() >= 0
        assert df['Final_Score'].max() <= 100
    
    def test_validate_input_valid(self):
        """Test input validation with valid data."""
        data = {
            'Study_Hours': 5.0,
            'Attendance': 80.0,
            'Prev_Score': 75.0,
            'Test_Prep': 1
        }
        assert validate_input_data(data) is True
    
    def test_validate_input_invalid(self):
        """Test input validation with invalid data."""
        data = {
            'Study_Hours': 20.0,  # Out of range
            'Attendance': 80.0,
            'Prev_Score': 75.0,
            'Test_Prep': 1
        }
        with pytest.raises(DataValidationError):
            validate_input_data(data)


class TestPreprocessing:
    """Test preprocessing pipeline."""
    
    def test_preprocessing_pipeline(self):
        """Test preprocessing pipeline."""
        df = generate_synthetic_data()
        X = df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']]
        
        pipeline = PreprocessingPipeline(scaling_method='standard')
        X_transformed = pipeline.fit_transform(X)
        
        assert X_transformed.shape == X.shape
        assert np.all(np.isfinite(X_transformed.values))


class TestFeatureEngineering:
    """Test feature engineering."""
    
    def test_feature_engineering(self):
        """Test feature engineering module."""
        df = generate_synthetic_data(n_samples=50)
        X = df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']]
        
        engineer = FeatureEngineer()
        X_engineered = engineer.engineer_features(X)
        
        assert X_engineered.shape[0] == X.shape[0]
        assert X_engineered.shape[1] > X.shape[1]  # Should have more features


class TestModels:
    """Test ML models."""
    
    @pytest.fixture
    def train_data(self):
        """Generate training data."""
        df = generate_synthetic_data(n_samples=100)
        X = df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']]
        y = df['Final_Score']
        return X, y
    
    def test_random_forest_model(self, train_data):
        """Test Random Forest model."""
        X, y = train_data
        model = RandomForestModel()
        model.train(X, y)
        
        predictions = model.predict(X)
        assert len(predictions) == len(y)
        assert np.all((predictions >= 0) & (predictions <= 100))
    
    def test_ensemble_model(self, train_data):
        """Test Ensemble model."""
        X, y = train_data
        model = EnsembleModel()
        model.train(X, y)
        
        predictions = model.predict(X)
        assert len(predictions) == len(y)
        
        metrics = model.evaluate(X, y)
        assert 'rmse' in metrics
        assert 'r2' in metrics


class TestEvaluation:
    """Test evaluation metrics."""
    
    def test_metrics_calculation(self):
        """Test metrics calculation."""
        y_true = np.array([70, 75, 80, 85, 90])
        y_pred = np.array([72, 73, 82, 84, 91])
        
        metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)
        
        assert 'RMSE' in metrics
        assert 'R2' in metrics
        assert 'MAE' in metrics
        assert metrics['RMSE'] > 0


class TestRiskAssessment:
    """Test risk assessment system."""
    
    def test_risk_score_calculation(self):
        """Test risk score calculation."""
        risk_score = RiskAssessment.calculate_risk_score(
            predicted_score=60,
            attendance=70,
            study_hours=3,
            prev_score=55
        )
        
        assert 0 <= risk_score <= 100
    
    def test_risk_level_classification(self):
        """Test risk level classification."""
        level, color = RiskAssessment.get_risk_level(90)
        assert level == "Low"
        
        level, color = RiskAssessment.get_risk_level(65)
        assert level == "Medium"
        
        level, color = RiskAssessment.get_risk_level(50)
        assert level == "High"


class TestRecommendations:
    """Test recommendation engine."""
    
    def test_recommendation_generation(self):
        """Test recommendation generation."""
        recommendations = RecommendationEngine.generate_recommendations(
            study_hours=5.0,
            attendance=80.0,
            prev_score=75.0,
            test_prep=1,
            predicted_score=80.0
        )
        
        assert len(recommendations) > 0
        assert all('title' in rec for rec in recommendations)
        assert all('suggestion' in rec for rec in recommendations)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
