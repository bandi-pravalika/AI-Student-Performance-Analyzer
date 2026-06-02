"""Prediction endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import pandas as pd
from src.data.generator import prepare_prediction_input
from src.ml.models.model import EnsembleModel
from src.ml.preprocessing.pipeline import PreprocessingPipeline
from src.ml.features.engineer import FeatureEngineer
from src.ml.evaluation.metrics import ModelEvaluator
from src.ml.explainability.analyzer import ExplainabilityAnalyzer, shap_like_explanation
from src.business.risk import RiskAssessment, InterventionSystem
from src.business.recommendations import RecommendationEngine
from src.core.exceptions import DataValidationError, PredictionError
from src.core.database import save_prediction, get_prediction_history, clear_prediction_history
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Request/Response Models
class PredictionRequest(BaseModel):
    """Request model for predictions."""
    student_name: Optional[str] = Field(default="Anonymous Student", description="Name of the student")
    Study_Hours: float = Field(..., ge=0, le=15, description="Weekly study hours")
    Attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    Prev_Score: float = Field(..., ge=0, le=100, description="Previous exam score")
    Test_Prep: int = Field(..., ge=0, le=1, description="Test preparation (0 or 1)")
    
    class Config:
        schema_extra = {
            "example": {
                "student_name": "John Doe",
                "Study_Hours": 5.0,
                "Attendance": 80.0,
                "Prev_Score": 75.0,
                "Test_Prep": 1
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    id: Optional[int] = None
    student_name: Optional[str] = None
    predicted_score: float
    grade: str
    risk_level: str
    risk_score: float
    confidence_interval: Dict[str, float]
    feature_importance: Dict[str, float]
    shap_explanation: Dict
    recommendations: List[Dict]
    intervention_actions: List[Dict]


# Global model cache
model_cache = None
preprocessing_cache = None


def get_model():
    """Get or load the model."""
    global model_cache, preprocessing_cache
    
    if model_cache is None:
        try:
            model_cache = EnsembleModel()
            # Generate and train on synthetic data for now
            from src.data.generator import generate_synthetic_data
            df = generate_synthetic_data()
            
            preprocessing_cache = PreprocessingPipeline()
            feature_engineer = FeatureEngineer()
            
            X = feature_engineer.engineer_features(df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']])
            X = preprocessing_cache.fit_transform(X)
            y = df['Final_Score']
            
            model_cache.train(X, y)
            logger.info("Model loaded and trained successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise PredictionError(f"Model initialization failed: {str(e)}")
    
    return model_cache, preprocessing_cache


router = APIRouter(tags=["Predictions"])


@router.post("/predictions", response_model=PredictionResponse)
def predict_performance(request: PredictionRequest):
    """
    Predict student performance and get comprehensive analysis.
    
    This endpoint:
    - Predicts final exam score using ensemble ML models
    - Assesses risk level
    - Generates personalized recommendations
    - Provides SHAP-like explanations
    """
    try:
        # Get model
        model, preprocessor = get_model()
        
        # Prepare input
        input_data = {
            'Study_Hours': request.Study_Hours,
            'Attendance': request.Attendance,
            'Prev_Score': request.Prev_Score,
            'Test_Prep': request.Test_Prep
        }
        
        # Validate input
        from src.data.generator import validate_input_data
        validate_input_data(input_data)
        
        # Prepare DataFrame
        df = prepare_prediction_input(input_data)
        
        # Feature engineering
        feature_engineer = FeatureEngineer()
        df_engineered = feature_engineer.engineer_features(df)
        
        # Preprocess
        df_scaled = preprocessor.transform(df_engineered)
        
        # Predict
        predicted_score = float(model.predict(df_scaled)[0])
        predicted_score = max(0, min(100, predicted_score))  # Clip to 0-100
        
        # Get component predictions for confidence
        component_preds = model.get_component_predictions(df_scaled)
        predictions_std = pd.Series([float(pred[0]) for pred in component_preds.values()]).std()
        
        # Calculate confidence interval
        confidence_interval = {
            'lower': float(predicted_score - 1.96 * predictions_std),
            'upper': float(predicted_score + 1.96 * predictions_std),
            'margin': float(1.96 * predictions_std)
        }
        
        # Get grade
        if predicted_score >= 85:
            grade = "A"
        elif predicted_score >= 70:
            grade = "B"
        elif predicted_score >= 55:
            grade = "C"
        else:
            grade = "F"
        
        # Risk assessment
        risk_metrics = RiskAssessment.get_risk_metrics({
            'predicted_score': predicted_score,
            'Attendance': request.Attendance,
            'Study_Hours': request.Study_Hours,
            'Prev_Score': request.Prev_Score
        })
        
        # Feature importance
        feature_importance = ExplainabilityAnalyzer.feature_importance_analysis(
            model.models['rf'].model,
            df_scaled.columns.tolist()
        )
        
        # SHAP-like explanation
        shap_explanation = shap_like_explanation(
            predicted_score,
            predicted_score,
            df_scaled,
            feature_importance,
            mean_prediction=70.0
        )
        
        # Recommendations
        recommendations = RecommendationEngine.generate_recommendations(
            request.Study_Hours,
            request.Attendance,
            request.Prev_Score,
            request.Test_Prep,
            predicted_score
        )
        
        # Intervention actions
        intervention_actions = InterventionSystem.determine_intervention_actions(
            input_data,
            risk_metrics
        )
        
        # Save to database
        pred_id = None
        try:
            pred_id = save_prediction(
                student_name=request.student_name,
                study_hours=request.Study_Hours,
                attendance=request.Attendance,
                prev_score=request.Prev_Score,
                test_prep=request.Test_Prep,
                predicted_score=predicted_score,
                grade=grade,
                risk_level=risk_metrics['risk_level'],
                risk_score=risk_metrics['risk_score']
            )
        except Exception as db_err:
            logger.error(f"Failed to auto-save prediction: {str(db_err)}")
        
        return PredictionResponse(
            id=pred_id,
            student_name=request.student_name,
            predicted_score=predicted_score,
            grade=grade,
            risk_level=risk_metrics['risk_level'],
            risk_score=risk_metrics['risk_score'],
            confidence_interval=confidence_interval,
            feature_importance=feature_importance,
            shap_explanation=shap_explanation,
            recommendations=recommendations,
            intervention_actions=intervention_actions
        )
    
    except DataValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/batch-predictions")
def batch_predict(requests: List[PredictionRequest]):
    """
    Make predictions for multiple students.
    """
    results = []
    for req in requests:
        try:
            result = predict_performance(req)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})
    
    return {"predictions": results}


@router.get("/history", response_model=List[Dict])
def get_history(limit: int = 100):
    """
    Get prediction history from database.
    """
    try:
        return get_prediction_history(limit=limit)
    except Exception as e:
        logger.error(f"Failed to fetch history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.delete("/history")
def delete_history():
    """
    Clear all prediction logs.
    """
    try:
        success = clear_prediction_history()
        return {"success": success, "message": "Prediction history cleared successfully" if success else "Failed to clear history"}
    except Exception as e:
        logger.error(f"Failed to clear history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")
