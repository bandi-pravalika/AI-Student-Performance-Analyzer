"""Risk prediction and assessment system."""
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from src.core.config import config


class RiskAssessment:
    """Comprehensive risk assessment for students."""
    
    @staticmethod
    def calculate_risk_score(predicted_score: float, attendance: float, 
                            study_hours: float, prev_score: float) -> float:
        """
        Calculate composite risk score (0-100, higher = more at-risk).
        
        Args:
            predicted_score: Model's predicted score
            attendance: Student attendance percentage
            study_hours: Weekly study hours
            prev_score: Previous exam score
            
        Returns:
            Risk score (0-100)
        """
        # Component 1: Predicted score (weight: 0.4)
        score_risk = (100 - predicted_score) * 0.4 if predicted_score < 70 else 0
        
        # Component 2: Attendance (weight: 0.3)
        attendance_risk = max(0, (75 - attendance) / 75 * 100) * 0.3
        
        # Component 3: Study hours (weight: 0.2)
        study_risk = max(0, (4 - study_hours) / 4 * 100) * 0.2
        
        # Component 4: Previous performance (weight: 0.1)
        prev_risk = max(0, (60 - prev_score) / 60 * 100) * 0.1
        
        total_risk = min(100, score_risk + attendance_risk + study_risk + prev_risk)
        return float(total_risk)
    
    @staticmethod
    def get_risk_level(predicted_score: float, risk_score: float = None) -> Tuple[str, str]:
        """
        Classify risk level.
        
        Args:
            predicted_score: Model's predicted score
            risk_score: Composite risk score
            
        Returns:
            Tuple of (risk_level, risk_color)
        """
        if predicted_score >= config.GRADE_A_MIN:
            return "Low", "🟢"
        elif predicted_score >= config.GRADE_B_MIN:
            return "Low", "🟢"
        elif predicted_score >= config.GRADE_C_MIN:
            return "Medium", "🟡"
        else:
            return "High", "🔴"
    
    @staticmethod
    def get_risk_metrics(student_data: Dict) -> Dict:
        """
        Calculate comprehensive risk metrics.
        
        Args:
            student_data: Dictionary with student features
            
        Returns:
            Dictionary with risk metrics
        """
        predicted_score = student_data.get('predicted_score', 70)
        attendance = student_data.get('Attendance', 75)
        study_hours = student_data.get('Study_Hours', 5)
        prev_score = student_data.get('Prev_Score', 70)
        
        risk_score = RiskAssessment.calculate_risk_score(
            predicted_score, attendance, study_hours, prev_score
        )
        risk_level, risk_color = RiskAssessment.get_risk_level(predicted_score, risk_score)
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'risk_indicators': {
                'low_attendance': attendance < 75,
                'low_study_hours': study_hours < 4,
                'low_previous_score': prev_score < 60,
                'poor_predicted_score': predicted_score < 55
            }
        }


class InterventionSystem:
    """System to identify students needing intervention."""
    
    @staticmethod
    def determine_intervention_actions(student_data: Dict, risk_metrics: Dict) -> list:
        """
        Determine intervention actions based on risk metrics.
        
        Args:
            student_data: Student feature data
            risk_metrics: Risk assessment metrics
            
        Returns:
            List of intervention actions
        """
        actions = []
        
        # High risk
        if risk_metrics['risk_level'] == 'High':
            actions.append({
                'priority': 'urgent',
                'action': 'Schedule immediate teacher meeting',
                'reason': 'Student at high risk of failing'
            })
            
            if risk_metrics['risk_indicators']['low_attendance']:
                actions.append({
                    'priority': 'high',
                    'action': 'Contact parent regarding attendance',
                    'reason': 'Attendance below 75%'
                })
            
            if risk_metrics['risk_indicators']['poor_predicted_score']:
                actions.append({
                    'priority': 'high',
                    'action': 'Enroll in tutoring program',
                    'reason': 'Predicted score below 55'
                })
        
        # Medium risk
        elif risk_metrics['risk_level'] == 'Medium':
            actions.append({
                'priority': 'medium',
                'action': 'Monitor progress closely',
                'reason': 'Student in medium risk zone'
            })
            
            if risk_metrics['risk_indicators']['low_study_hours']:
                actions.append({
                    'priority': 'medium',
                    'action': 'Recommend study group participation',
                    'reason': 'Study hours below recommended'
                })
        
        return actions
