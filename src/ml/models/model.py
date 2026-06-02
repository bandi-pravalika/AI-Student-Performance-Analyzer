"""ML model implementations and management."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import json
from pathlib import Path
from typing import Dict, Tuple
from src.core.config import config
from src.core.constants import FEATURE_NAMES


class BaseModel:
    """Base class for all ML models."""
    
    def __init__(self, model_name: str):
        """Initialize base model."""
        self.model_name = model_name
        self.model = None
        self.is_trained = False
        self.training_metrics = {}
        self.feature_importance = None
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train the model. Implemented by subclasses."""
        raise NotImplementedError
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        if not self.is_trained:
            raise ValueError(f"Model {self.model_name} not trained yet")
        return self.model.predict(X)
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """Evaluate model on test set."""
        predictions = self.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        mae = np.mean(np.abs(y_test - predictions))
        
        self.training_metrics = {
            'rmse': float(rmse),
            'r2': float(r2),
            'mae': float(mae)
        }
        
        return self.training_metrics
    
    def save(self, path: str):
        """Save model to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load(self, path: str):
        """Load model from disk."""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True


class RandomForestModel(BaseModel):
    """Random Forest Regressor model."""
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """Initialize Random Forest model."""
        super().__init__("RandomForest")
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            n_jobs=-1
        )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train Random Forest model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True
        self.feature_importance = dict(zip(X_train.columns, self.model.feature_importances_))


class GradientBoostingModel(BaseModel):
    """Gradient Boosting Regressor model."""
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """Initialize Gradient Boosting model."""
        super().__init__("GradientBoosting")
        self.model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2
        )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train Gradient Boosting model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True
        self.feature_importance = dict(zip(X_train.columns, self.model.feature_importances_))


class LinearRegressionModel(BaseModel):
    """Linear Regression model."""
    
    def __init__(self):
        """Initialize Linear Regression model."""
        super().__init__("LinearRegression")
        self.model = LinearRegression()
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train Linear Regression model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True
        self.feature_importance = dict(zip(X_train.columns, np.abs(self.model.coef_)))


class EnsembleModel(BaseModel):
    """Ensemble model combining multiple models."""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize Ensemble model.
        
        Args:
            weights: Dictionary of model weights for averaging
        """
        super().__init__("Ensemble")
        self.models = {
            'rf': RandomForestModel(),
            'gb': GradientBoostingModel(),
            'lr': LinearRegressionModel()
        }
        self.weights = weights or {'rf': 0.5, 'gb': 0.3, 'lr': 0.2}
        
        # Normalize weights
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train all models in ensemble."""
        for model in self.models.values():
            model.train(X_train, y_train)
        self.is_trained = True
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make ensemble predictions by weighted averaging."""
        predictions = np.zeros(len(X))
        
        for name, model in self.models.items():
            pred = model.predict(X)
            predictions += self.weights[name] * pred
        
        return predictions
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """Evaluate ensemble model."""
        predictions = self.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        mae = np.mean(np.abs(y_test - predictions))
        
        self.training_metrics = {
            'rmse': float(rmse),
            'r2': float(r2),
            'mae': float(mae)
        }
        
        return self.training_metrics
    
    def get_component_predictions(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Get predictions from each component model."""
        return {name: model.predict(X) for name, model in self.models.items()}
