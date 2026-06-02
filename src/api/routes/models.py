"""Model management endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict
from src.api.routes.predictions import get_model
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Models"])


@router.get("/models/info")
def get_model_info():
    """Get information about trained models."""
    try:
        model, _ = get_model()
        
        # Get metrics for each component
        component_info = {}
        for name, m in model.models.items():
            component_info[name] = {
                'name': m.model_name,
                'type': m.model.__class__.__name__,
                'is_trained': m.is_trained,
                'metrics': m.training_metrics
            }
        
        return {
            'ensemble_model': 'Active',
            'weights': model.weights,
            'components': component_info,
            'status': 'Ready'
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/feature-importance")
def get_feature_importance():
    """Get feature importance from models."""
    try:
        model, _ = get_model()
        
        importance = {}
        for name, m in model.models.items():
            if m.feature_importance:
                importance[name] = m.feature_importance
        
        return importance
    except Exception as e:
        logger.error(f"Error getting feature importance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/metrics")
def get_model_metrics():
    """Get model evaluation metrics."""
    try:
        model, _ = get_model()
        
        metrics = {}
        for name, m in model.models.items():
            metrics[name] = m.training_metrics
        
        return metrics
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
