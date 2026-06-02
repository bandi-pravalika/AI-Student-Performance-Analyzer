"""Feature engineering utilities."""
import pandas as pd
import numpy as np
from src.core.constants import FEATURE_NAMES


class FeatureEngineer:
    """Creates derived features for improved model performance."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.base_features = FEATURE_NAMES.copy()
        self.derived_features = []
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between existing features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with interaction features
        """
        df_engineered = df.copy()
        
        # Study hours * Previous score (high studier + good history = strong predictor)
        df_engineered['Study_x_PrevScore'] = df_engineered['Study_Hours'] * df_engineered['Prev_Score']
        
        # Attendance * Test prep (engaged student with prep)
        df_engineered['Attendance_x_TestPrep'] = df_engineered['Attendance'] * df_engineered['Test_Prep']
        
        # Study hours * Test prep (dedicated preparation)
        df_engineered['Study_x_TestPrep'] = df_engineered['Study_Hours'] * df_engineered['Test_Prep']
        
        self.derived_features.extend(['Study_x_PrevScore', 'Attendance_x_TestPrep', 'Study_x_TestPrep'])
        
        return df_engineered
    
    def create_polynomial_features(self, df: pd.DataFrame, degree: int = 2) -> pd.DataFrame:
        """
        Create polynomial features.
        
        Args:
            df: Input DataFrame
            degree: Polynomial degree
            
        Returns:
            DataFrame with polynomial features
        """
        df_engineered = df.copy()
        
        # Quadratic features for continuous variables
        for feature in ['Study_Hours', 'Attendance', 'Prev_Score']:
            df_engineered[f'{feature}_squared'] = df_engineered[feature] ** degree
            self.derived_features.append(f'{feature}_squared')
        
        return df_engineered
    
    def create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create ratio features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with ratio features
        """
        df_engineered = df.copy()
        
        # Study hours to attendance ratio (efficiency metric)
        # Add small epsilon to avoid division by zero
        df_engineered['Study_to_Attendance_Ratio'] = df_engineered['Study_Hours'] / (df_engineered['Attendance'] + 0.1)
        
        # Previous score relative to attendance (achievement vs. presence)
        df_engineered['PrevScore_to_Attendance'] = df_engineered['Prev_Score'] / (df_engineered['Attendance'] + 0.1)
        
        self.derived_features.extend(['Study_to_Attendance_Ratio', 'PrevScore_to_Attendance'])
        
        return df_engineered
    
    def create_binned_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create binned categorical features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with binned features
        """
        df_engineered = df.copy()
        
        # Bin study hours
        df_engineered['Study_Level'] = pd.cut(df_engineered['Study_Hours'], 
                                               bins=[0, 3, 6, 10, 15],
                                               labels=[1, 2, 3, 4]).astype(int)
        
        # Bin attendance
        df_engineered['Attendance_Level'] = pd.cut(df_engineered['Attendance'], 
                                                    bins=[0, 50, 75, 90, 100],
                                                    labels=[1, 2, 3, 4]).astype(int)
        
        self.derived_features.extend(['Study_Level', 'Attendance_Level'])
        
        return df_engineered
    
    def engineer_features(self, df: pd.DataFrame, include_interactions: bool = True,
                         include_polynomial: bool = True, include_ratios: bool = True,
                         include_binned: bool = True) -> pd.DataFrame:
        """
        Apply all feature engineering steps.
        
        Args:
            df: Input DataFrame
            include_interactions: Include interaction features
            include_polynomial: Include polynomial features
            include_ratios: Include ratio features
            include_binned: Include binned features
            
        Returns:
            DataFrame with engineered features
        """
        df_engineered = df.copy()
        
        if include_interactions:
            df_engineered = self.create_interaction_features(df_engineered)
        
        if include_polynomial:
            df_engineered = self.create_polynomial_features(df_engineered)
        
        if include_ratios:
            df_engineered = self.create_ratio_features(df_engineered)
        
        if include_binned:
            df_engineered = self.create_binned_features(df_engineered)
        
        return df_engineered
    
    def get_all_features(self) -> list:
        """Get list of all features (base + derived)."""
        return self.base_features + self.derived_features
    
    def get_derived_features(self) -> list:
        """Get list of derived features only."""
        return self.derived_features.copy()
