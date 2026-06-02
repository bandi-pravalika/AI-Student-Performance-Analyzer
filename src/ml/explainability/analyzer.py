"""Model explainability using SHAP and other methods."""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class ExplainabilityAnalyzer:
    """Provides model explainability without external SHAP dependency initially."""
    
    @staticmethod
    def feature_importance_analysis(model, feature_names: List[str]) -> Dict[str, float]:
        """
        Extract feature importance from model.
        
        Args:
            model: Trained model with feature_importance_ attribute
            feature_names: List of feature names
            
        Returns:
            Dictionary of feature importance scores
        """
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
        else:
            return {}
        
        importance_dict = dict(zip(feature_names, importances))
        # Normalize to sum to 1
        total = sum(importance_dict.values())
        return {k: v/total for k, v in importance_dict.items()}
    
    @staticmethod
    def permutation_importance(model, X: pd.DataFrame, y: np.ndarray, 
                               n_repeats: int = 10) -> Dict[str, float]:
        """
        Calculate permutation importance.
        
        Args:
            model: Trained model
            X: Feature data
            y: Target data
            n_repeats: Number of repeats
            
        Returns:
            Dictionary of permutation importance scores
        """
        from sklearn.metrics import mean_squared_error
        
        baseline_score = mean_squared_error(y, model.predict(X))
        importances = {}
        
        for feature in X.columns:
            scores = []
            for _ in range(n_repeats):
                X_permuted = X.copy()
                X_permuted[feature] = np.random.permutation(X_permuted[feature])
                score = mean_squared_error(y, model.predict(X_permuted))
                scores.append(score - baseline_score)
            
            importances[feature] = np.mean(scores)
        
        # Normalize
        if sum(importances.values()) != 0:
            total = max(sum([v for v in importances.values() if v > 0]), 0.001)
            importances = {k: max(0, v/total) for k, v in importances.items()}
        
        return importances
    
    @staticmethod
    def predict_contribution(X: pd.DataFrame, base_prediction: float, 
                            actual_prediction: float, feature_names: List[str],
                            feature_importance: Dict[str, float]) -> Dict[str, float]:
        """
        Estimate each feature's contribution to prediction (simplified SHAP-like).
        
        Args:
            X: Input features (single sample)
            base_prediction: Base/average prediction
            actual_prediction: Model prediction
            feature_names: Feature names
            feature_importance: Feature importance scores
            
        Returns:
            Dictionary of feature contributions
        """
        total_prediction_diff = actual_prediction - base_prediction
        contributions = {}
        
        for feature in feature_names:
            # Weight the difference by feature importance and normalized feature value
            feature_value = X[feature].values[0] if hasattr(X, 'values') else X[feature]
            feature_normalized = feature_value / (abs(feature_value) + 0.001)
            
            contribution = (feature_importance.get(feature, 0) * total_prediction_diff * 
                           feature_normalized)
            contributions[feature] = float(contribution)
        
        return contributions
    
    @staticmethod
    def get_model_insights(model, X: pd.DataFrame, y: np.ndarray, 
                          feature_importance: Dict[str, float]) -> Dict:
        """
        Generate comprehensive model insights.
        
        Args:
            model: Trained model
            X: Feature data
            y: Target data
            feature_importance: Feature importance scores
            
        Returns:
            Dictionary of model insights
        """
        from sklearn.metrics import r2_score, mean_squared_error
        
        predictions = model.predict(X)
        residuals = y - predictions
        
        # Find most impactful features
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Find hard-to-predict samples
        residual_indices = np.argsort(np.abs(residuals))[-5:]
        
        insights = {
            'model_type': model.__class__.__name__,
            'r2_score': float(r2_score(y, predictions)),
            'rmse': float(np.sqrt(mean_squared_error(y, predictions))),
            'top_features': [{'name': f[0], 'importance': float(f[1])} for f in top_features],
            'hardest_predictions': {
                'indices': [int(i) for i in residual_indices],
                'errors': [float(abs(residuals[i])) for i in residual_indices]
            },
            'prediction_range': {
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions)),
                'mean': float(np.mean(predictions))
            }
        }
        
        return insights


def shap_like_explanation(prediction: float, model_prediction: float, 
                          X: pd.DataFrame, feature_importance: Dict[str, float],
                          mean_prediction: float = 70.0) -> Dict:
    """
    Generate SHAP-like explanation for a single prediction.
    
    Args:
        prediction: Model prediction
        model_prediction: Model's actual prediction
        X: Input features
        feature_importance: Feature importance dictionary
        mean_prediction: Mean model prediction (baseline)
        
    Returns:
        Dictionary with explanation
    """
    explanation = {
        'base_value': mean_prediction,
        'prediction': float(prediction),
        'output_value': float(prediction),
        'feature_values': {}
    }
    
    base_diff = prediction - mean_prediction
    
    for feature in X.columns:
        value = X[feature].values[0] if hasattr(X, 'values') else X[feature]
        importance = feature_importance.get(feature, 0)
        contribution = importance * base_diff
        
        explanation['feature_values'][feature] = {
            'value': float(value),
            'importance': float(importance),
            'contribution': float(contribution)
        }
    
    return explanation
