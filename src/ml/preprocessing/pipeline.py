"""Data preprocessing pipeline."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from src.core.config import config
from src.core.constants import FEATURE_NAMES, TARGET_NAME


class PreprocessingPipeline:
    """Handles data preprocessing and scaling."""
    
    def __init__(self, scaling_method: str = "standard"):
        """
        Initialize preprocessing pipeline.
        
        Args:
            scaling_method: 'standard' or 'minmax'
        """
        self.scaling_method = scaling_method
        self.scaler = None
        self.feature_names = FEATURE_NAMES
        
    def fit(self, X: pd.DataFrame) -> 'PreprocessingPipeline':
        """
        Fit the scaler on training data.
        
        Args:
            X: Training features
            
        Returns:
            Self for chaining
        """
        if self.scaling_method == "standard":
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler()
        
        self.scaler.fit(X[self.feature_names])
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform features using fitted scaler.
        
        Args:
            X: Features to transform
            
        Returns:
            Transformed features
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(X[self.feature_names])
        X_transformed = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        return X_transformed
    
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Fit and transform in one step.
        
        Args:
            X: Features to fit and transform
            
        Returns:
            Transformed features
        """
        self.fit(X)
        return self.transform(X)


def remove_outliers_iqr(df: pd.DataFrame, columns: list = None, iqr_multiplier: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers using Interquartile Range method.
    
    Args:
        df: DataFrame to clean
        columns: Columns to check for outliers
        iqr_multiplier: IQR multiplier threshold
        
    Returns:
        DataFrame without outliers
    """
    if columns is None:
        columns = [TARGET_NAME]
    
    df_clean = df.copy()
    
    for col in columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR
        df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
    
    return df_clean


def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Handle missing values in dataset.
    
    Args:
        df: DataFrame with potential missing values
        strategy: 'mean', 'median', or 'drop'
        
    Returns:
        DataFrame with missing values handled
    """
    df_clean = df.copy()
    
    if strategy == "drop":
        df_clean = df_clean.dropna()
    elif strategy in ["mean", "median"]:
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_clean[col].isnull().sum() > 0:
                if strategy == "mean":
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                else:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    return df_clean
