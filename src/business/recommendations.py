"""Personalized recommendation engine."""
from typing import List, Dict
from src.core.config import config
from src.core.constants import RECOMMENDATION_CATEGORIES


class RecommendationEngine:
    """Generates personalized, rule-based recommendations."""
    
    @staticmethod
    def generate_recommendations(study_hours: float, attendance: float, 
                                prev_score: float, test_prep: int,
                                predicted_score: float = None) -> List[Dict]:
        """
        Generate personalized recommendations based on student profile.
        
        Args:
            study_hours: Weekly study hours
            attendance: Attendance percentage
            prev_score: Previous exam score
            test_prep: Whether student completed test prep (0 or 1)
            predicted_score: Model's prediction (optional)
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # ===== STUDY TIME RECOMMENDATIONS =====
        if study_hours < config.STUDY_HOURS_THRESHOLD_LOW:
            recommendations.append({
                'category': 'study_time',
                'priority': 'high',
                'icon': '🕒',
                'title': 'Increase Study Time',
                'description': f'Your current study hours ({study_hours:.1f}/week) are quite low.',
                'suggestion': f'Aim for at least {config.STUDY_HOURS_THRESHOLD_LOW}-{config.STUDY_HOURS_THRESHOLD_LOW + 1} hours of dedicated study per week.',
                'impact': 'Increased study time correlates with 5-10 point score improvement',
                'action_items': [
                    'Create a weekly study schedule',
                    'Set specific, measurable study goals',
                    'Track daily study sessions'
                ]
            })
        elif study_hours > config.STUDY_HOURS_THRESHOLD_HIGH:
            recommendations.append({
                'category': 'study_time',
                'priority': 'medium',
                'icon': '⚖️',
                'title': 'Balance Study Load',
                'description': f'Your study hours ({study_hours:.1f}/week) are quite high.',
                'suggestion': 'Focus on quality over quantity. Ensure you are taking adequate breaks to avoid burnout.',
                'impact': 'Balanced approach maintains performance while reducing stress',
                'action_items': [
                    'Implement Pomodoro technique (25min study + 5min break)',
                    'Take longer breaks every 2-3 hours',
                    'Monitor stress levels daily'
                ]
            })
        else:
            recommendations.append({
                'category': 'study_time',
                'priority': 'low',
                'icon': '✅',
                'title': 'Study Schedule is Good',
                'description': f'Your study hours ({study_hours:.1f}/week) are in a healthy range.',
                'suggestion': 'Maintain this consistent approach to studying.',
                'impact': 'Consistent study habits lead to stable performance',
                'action_items': [
                    'Continue with your current routine',
                    'Occasionally review and adjust techniques'
                ]
            })
        
        # ===== ATTENDANCE RECOMMENDATIONS =====
        if attendance < config.ATTENDANCE_THRESHOLD:
            recommendations.append({
                'category': 'attendance',
                'priority': 'high',
                'icon': '🏫',
                'title': 'Improve Attendance',
                'description': f'Your attendance ({attendance:.1f}%) is below the optimal threshold.',
                'suggestion': f'Aim to attend at least {config.ATTENDANCE_THRESHOLD:.0f}% of classes.',
                'impact': 'Every 10% increase in attendance correlates with 2-3 point score increase',
                'action_items': [
                    'Set a personal attendance goal',
                    'Identify and address barriers to attendance',
                    'Connect with friends for accountability'
                ]
            })
        else:
            recommendations.append({
                'category': 'attendance',
                'priority': 'low',
                'icon': '✅',
                'title': 'Great Attendance!',
                'description': f'Your attendance ({attendance:.1f}%) is excellent.',
                'suggestion': 'Keep up this commitment to class participation.',
                'impact': 'Consistent attendance reinforces learning',
                'action_items': [
                    'Continue attending all classes',
                    'Arrive early to review notes'
                ]
            })
        
        # ===== PREVIOUS PERFORMANCE RECOMMENDATIONS =====
        if prev_score < config.PREV_SCORE_THRESHOLD:
            recommendations.append({
                'category': 'previous_score',
                'priority': 'high',
                'icon': '📚',
                'title': 'Focus on Revision',
                'description': f'Your previous score ({prev_score:.1f}) suggests foundational gaps.',
                'suggestion': 'Review previous exam topics and ask teachers for clarification.',
                'impact': 'Addressing basics improves overall performance',
                'action_items': [
                    'Review previous exam paper',
                    'Request help on weak topics',
                    'Use supplementary study materials'
                ]
            })
        else:
            recommendations.append({
                'category': 'previous_score',
                'priority': 'low',
                'icon': '⭐',
                'title': 'Strong Foundation',
                'description': f'Your previous score ({prev_score:.1f}) shows a solid foundation.',
                'suggestion': 'Build on this strength with targeted preparation.',
                'impact': 'Good foundation reduces exam anxiety',
                'action_items': [
                    'Focus on advanced topics',
                    'Practice difficult problems'
                ]
            })
        
        # ===== TEST PREPARATION RECOMMENDATIONS =====
        if test_prep == 0:
            recommendations.append({
                'category': 'test_prep',
                'priority': 'high',
                'icon': '📝',
                'title': 'Complete Test Preparation',
                'description': 'You haven\'t taken a test preparation course.',
                'suggestion': 'Consider enrolling in a test prep course or workshop.',
                'impact': 'Test prep students show 8-12 point average improvement',
                'action_items': [
                    'Research available test prep resources',
                    'Enroll in a structured prep course',
                    'Practice with past exam papers'
                ]
            })
        else:
            recommendations.append({
                'category': 'test_prep',
                'priority': 'medium',
                'icon': '🎯',
                'title': 'Leverage Test Prep',
                'description': 'You\'ve completed test preparation.',
                'suggestion': 'Apply test-taking strategies learned from prep course.',
                'impact': 'Effective strategy application maximizes test prep value',
                'action_items': [
                    'Review test-taking strategies',
                    'Practice time management',
                    'Do full-length practice tests'
                ]
            })
        
        # ===== GENERAL RECOMMENDATIONS =====
        if predicted_score and predicted_score < 55:
            recommendations.append({
                'category': 'general',
                'priority': 'urgent',
                'icon': '🆘',
                'title': 'Seek Immediate Help',
                'description': 'Your predicted score indicates high risk of failing.',
                'suggestion': 'Connect with your teacher, academic advisor, or tutoring services immediately.',
                'impact': 'Early intervention can prevent course failure',
                'action_items': [
                    'Contact your teacher this week',
                    'Visit tutoring center',
                    'Meet with academic advisor'
                ]
            })
        elif predicted_score and predicted_score >= 85:
            recommendations.append({
                'category': 'general',
                'priority': 'low',
                'icon': '🎉',
                'title': 'Excellent Performance Expected!',
                'description': 'Your habits and scores predict excellent performance.',
                'suggestion': 'Continue your current approach and maintain consistency.',
                'impact': 'Your trajectory suggests strong academic success',
                'action_items': [
                    'Maintain your current habits',
                    'Consider peer mentoring',
                    'Challenge yourself with advanced topics'
                ]
            })
        
        # Sort by priority
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 4))
        
        return recommendations
    
    @staticmethod
    def format_recommendations_for_display(recommendations: List[Dict]) -> str:
        """
        Format recommendations for Streamlit display.
        
        Args:
            recommendations: List of recommendation dictionaries
            
        Returns:
            Formatted string for display
        """
        output = ""
        
        for rec in recommendations:
            output += f"\n### {rec['icon']} {rec['title']}\n"
            output += f"**{rec['description']}**\n\n"
            output += f"💡 *{rec['suggestion']}*\n\n"
            output += f"**Expected Impact:** {rec['impact']}\n\n"
            output += "**Action Items:**\n"
            for item in rec['action_items']:
                output += f"- {item}\n"
            output += "\n---\n"
        
        return output
