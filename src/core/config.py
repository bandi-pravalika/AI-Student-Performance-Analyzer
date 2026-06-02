"""Configuration management for the application."""
import os
from typing import Optional

class Config:
    """Base configuration."""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"
    
    # ML Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "ml_models/v1")
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))
    TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
    
    # Feature Configuration
    FEATURE_SCALING = os.getenv("FEATURE_SCALING", "standard")  # standard, minmax
    
    # Risk Thresholds
    RISK_THRESHOLD_HIGH = float(os.getenv("RISK_THRESHOLD_HIGH", 55))
    RISK_THRESHOLD_MEDIUM = float(os.getenv("RISK_THRESHOLD_MEDIUM", 70))
    
    # Grade Thresholds
    GRADE_A_MIN = float(os.getenv("GRADE_A_MIN", 85))
    GRADE_B_MIN = float(os.getenv("GRADE_B_MIN", 70))
    GRADE_C_MIN = float(os.getenv("GRADE_C_MIN", 55))
    
    # Recommendation Rules
    STUDY_HOURS_THRESHOLD_LOW = float(os.getenv("STUDY_HOURS_THRESHOLD_LOW", 4.0))
    STUDY_HOURS_THRESHOLD_HIGH = float(os.getenv("STUDY_HOURS_THRESHOLD_HIGH", 8.0))
    ATTENDANCE_THRESHOLD = float(os.getenv("ATTENDANCE_THRESHOLD", 75.0))
    PREV_SCORE_THRESHOLD = float(os.getenv("PREV_SCORE_THRESHOLD", 60.0))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "student_analyzer.db")


config = Config()

