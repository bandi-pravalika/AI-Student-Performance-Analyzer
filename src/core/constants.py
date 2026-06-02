"""Application constants."""

# Feature names
FEATURE_NAMES = [
    'Study_Hours',
    'Attendance',
    'Prev_Score',
    'Test_Prep'
]

TARGET_NAME = 'Final_Score'

# Grade mapping
GRADE_MAPPING = {
    'A': (85, 100),
    'B': (70, 85),
    'C': (55, 70),
    'F': (0, 55)
}

# Risk level mapping
RISK_LEVEL_MAPPING = {
    'High': (0, 55),
    'Medium': (55, 70),
    'Low': (70, 100)
}

# Model types
MODEL_TYPES = [
    'random_forest',
    'gradient_boosting',
    'linear_regression',
    'ensemble'
]

# Recommendation categories
RECOMMENDATION_CATEGORIES = {
    'study_time': 'Study Time',
    'attendance': 'Attendance',
    'previous_score': 'Previous Performance',
    'test_prep': 'Test Preparation',
    'general': 'General'
}
