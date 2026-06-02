"""Model evaluation and metrics."""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
from typing import Dict, Tuple


class ModelEvaluator:
    """Comprehensive model evaluation utilities."""
    
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Mean Absolute Percentage Error (custom for bounded scores)
        residuals = np.abs(y_true - y_pred)
        
        return {
            'MSE': float(mse),
            'RMSE': float(rmse),
            'MAE': float(mae),
            'MAPE': float(mape),
            'R2': float(r2),
            'Mean_Residual': float(np.mean(residuals)),
            'Std_Residual': float(np.std(residuals))
        }
    
    @staticmethod
    def calculate_prediction_intervals(y_true: np.ndarray, y_pred: np.ndarray, 
                                       confidence: float = 0.95) -> Dict[str, np.ndarray]:
        """
        Calculate prediction intervals based on residuals.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            confidence: Confidence level (0-1)
            
        Returns:
            Dictionary with lower and upper bounds
        """
        residuals = y_true - y_pred
        std_residual = np.std(residuals)
        
        # Using normal distribution approximation
        z_score = 1.96 if confidence == 0.95 else 1.645 if confidence == 0.90 else 2.576
        margin = z_score * std_residual
        
        return {
            'lower_bound': y_pred - margin,
            'upper_bound': y_pred + margin,
            'margin': margin
        }
    
    @staticmethod
    def residual_analysis(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Analyze model residuals.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary with residual statistics
        """
        residuals = y_true - y_pred
        
        return {
            'mean': float(np.mean(residuals)),
            'std': float(np.std(residuals)),
            'min': float(np.min(residuals)),
            'max': float(np.max(residuals)),
            'median': float(np.median(residuals)),
            'q25': float(np.percentile(residuals, 25)),
            'q75': float(np.percentile(residuals, 75))
        }
    
    @staticmethod
    def prediction_accuracy_by_range(y_true: np.ndarray, y_pred: np.ndarray, 
                                     bins: list = None) -> Dict:
        """
        Analyze prediction accuracy across different score ranges.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            bins: Score ranges to analyze
            
        Returns:
            Dictionary with accuracy metrics per range
        """
        if bins is None:
            bins = [0, 55, 70, 85, 100]
        
        results = {}
        for i in range(len(bins) - 1):
            mask = (y_true >= bins[i]) & (y_true < bins[i + 1])
            if np.sum(mask) > 0:
                rmse = np.sqrt(mean_squared_error(y_true[mask], y_pred[mask]))
                mae = mean_absolute_error(y_true[mask], y_pred[mask])
                r2 = r2_score(y_true[mask], y_pred[mask]) if np.std(y_true[mask]) > 0 else 0
                
                results[f'{bins[i]}-{bins[i+1]}'] = {
                    'RMSE': float(rmse),
                    'MAE': float(mae),
                    'R2': float(r2),
                    'Samples': int(np.sum(mask))
                }
        
        return results
    
    @staticmethod
    def model_comparison(models_results: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare multiple models' performance.
        
        Args:
            models_results: Dictionary with model names and their metrics
            
        Returns:
            DataFrame with comparison
        """
        comparison_df = pd.DataFrame(models_results).T
        comparison_df = comparison_df.sort_values('R2', ascending=False)
        return comparison_df
