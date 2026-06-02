"""Data generation and utility functions."""
import numpy as np
import pandas as pd
from src.core.config import config
from src.core.constants import FEATURE_NAMES, TARGET_NAME


def generate_synthetic_data(n_samples: int = 500) -> pd.DataFrame:
    """
    Generate synthetic student performance data.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with synthetic data
    """
    np.random.seed(config.RANDOM_SEED)
    
    # Generate features
    study_hours = np.random.uniform(1.0, 10.0, n_samples)
    attendance = np.random.uniform(50.0, 100.0, n_samples)
    prev_scores = np.random.uniform(40.0, 100.0, n_samples)
    test_prep = np.random.choice([0, 1], size=n_samples)
    
    # Create target with realistic formula
    # Score = base + study_contribution + attendance_contribution + history_contribution + prep_bonus + noise
    base_score = 10
    study_contribution = study_hours * 3
    attendance_contribution = attendance * 0.4
    history_contribution = prev_scores * 0.3
    prep_bonus = test_prep * 5
    noise = np.random.normal(0, 3, n_samples)
    
    final_score = base_score + study_contribution + attendance_contribution + \
                  history_contribution + prep_bonus + noise
    
    # Clip scores to 0-100 range
    final_score = np.clip(final_score, 0, 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Study_Hours': study_hours,
        'Attendance': attendance,
        'Prev_Score': prev_scores,
        'Test_Prep': test_prep,
        'Final_Score': final_score
    })
    
    return df


def validate_input_data(data: dict) -> bool:
    """
    Validate input data for predictions.
    
    Args:
        data: Dictionary with feature values
        
    Returns:
        True if valid, raises exception otherwise
    """
    from src.core.exceptions import DataValidationError
    
    required_fields = FEATURE_NAMES
    
    # Check all required fields present
    if not all(field in data for field in required_fields):
        raise DataValidationError(f"Missing required fields. Expected: {required_fields}")
    
    # Validate ranges
    if not 0 <= data['Study_Hours'] <= 15:
        raise DataValidationError("Study_Hours must be between 0 and 15")
    
    if not 0 <= data['Attendance'] <= 100:
        raise DataValidationError("Attendance must be between 0 and 100")
    
    if not 0 <= data['Prev_Score'] <= 100:
        raise DataValidationError("Prev_Score must be between 0 and 100")
    
    if data['Test_Prep'] not in [0, 1]:
        raise DataValidationError("Test_Prep must be 0 or 1")
    
    return True


def prepare_prediction_input(data: dict) -> pd.DataFrame:
    """
    Prepare input data for model prediction.
    
    Args:
        data: Dictionary with feature values
        
    Returns:
        DataFrame formatted for prediction
    """
    validate_input_data(data)
    
    df = pd.DataFrame([[
        data['Study_Hours'],
        data['Attendance'],
        data['Prev_Score'],
        data['Test_Prep']
    ]], columns=FEATURE_NAMES)
    
    return df
