import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Set page configuration
st.set_page_config(page_title="AI Student Performance Analyzer", page_icon="🎓", layout="wide")

# ==========================================
# 1. Dataset Generation and Model Training
# ==========================================

@st.cache_resource
def load_model():
    """Generates synthetic data and trains a RandomForest model."""
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Generate 500 sample records
    n_samples = 500
    study_hours = np.random.uniform(1.0, 10.0, n_samples)
    attendance = np.random.uniform(50.0, 100.0, n_samples)
    prev_scores = np.random.uniform(40.0, 100.0, n_samples)
    test_prep = np.random.choice([0, 1], size=n_samples) # 0: No, 1: Yes
    
    # Create a realistic target score formula with some noise
    # Score depends positively on all features
    base_score = 10 + (study_hours * 3) + (attendance * 0.4) + (prev_scores * 0.3) + (test_prep * 5)
    noise = np.random.normal(0, 3, n_samples)
    final_score = base_score + noise
    
    # Clip scores to be between 0 and 100
    final_score = np.clip(final_score, 0, 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Study_Hours': study_hours,
        'Attendance': attendance,
        'Prev_Score': prev_scores,
        'Test_Prep': test_prep,
        'Final_Score': final_score
    })
    
    # Train Model
    X = df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']]
    y = df['Final_Score']
    
    # We won't strictly evaluate it here, just fit it on the whole synthetic set for the app
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model

# Load the trained model
model = load_model()

# ==========================================
# 2. Recommendation & Logic System
# ==========================================

def evaluate_performance(predicted_score):
    """Assigns Grade and Risk Level based on the predicted score."""
    if predicted_score >= 85:
        grade = "A"
        risk_level = "Low"
    elif predicted_score >= 70:
        grade = "B"
        risk_level = "Low"
    elif predicted_score >= 55:
        grade = "C"
        risk_level = "Medium"
    else:
        grade = "Fail"
        risk_level = "High"
    return grade, risk_level

def generate_recommendations(study_hours, attendance, prev_score, test_prep):
    """Generates personalized rule-based recommendations."""
    recommendations = []
    
    # Rule 1: Study hours
    if study_hours < 4.0:
        recommendations.append("🕒 **Increase Study Time:** Your study hours are quite low. Try to aim for at least 4-5 hours of dedicated study time per week to improve retention.")
    elif study_hours > 8.0:
        recommendations.append("🌟 **Maintain Balance:** You are studying a lot! Make sure you are taking adequate breaks to avoid burnout.")

    # Rule 2: Attendance
    if attendance < 75.0:
        recommendations.append("🏫 **Improve Attendance:** Missing classes means missing crucial concepts. Aim to attend at least 80% of your classes.")
    
    # Rule 3: Previous Score
    if prev_score < 60.0:
        recommendations.append("📚 **Revision Strategies:** Since your previous scores were on the lower side, consider revising past topics and asking teachers for help on weak areas.")
    
    # Rule 4: Test Preparation
    if test_prep == "No":
        recommendations.append("📝 **Complete Preparation Course:** You haven't taken a test preparation course. Completing one can significantly boost your exam readiness and confidence.")
        
    # Default positive recommendation if doing well
    if not recommendations:
        recommendations.append("🎉 **Keep up the great work!** Your current habits are setting you up for success. Stay consistent!")
        
    return recommendations

# ==========================================
# 3. Streamlit User Interface
# ==========================================

st.title("🎓 AI Student Performance Analyzer")
st.markdown("Predict student exam scores and get personalized, AI-driven recommendations based on study habits!")

st.divider()

# Input section
st.header("📋 Enter Student Details")
col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider("Weekly Study Hours", min_value=0.0, max_value=15.0, value=5.0, step=0.5)
    attendance = st.slider("Attendance Percentage (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)

with col2:
    prev_score = st.number_input("Previous Exam Score (0-100)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    test_prep_str = st.selectbox("Completed Test Preparation Course?", ("Yes", "No"))

test_prep_val = 1 if test_prep_str == "Yes" else 0

st.divider()

# Prediction button
if st.button("🔮 Predict Performance & Get Recommendations", type="primary"):
    
    # Prepare input for the model
    input_data = pd.DataFrame([[study_hours, attendance, prev_score, test_prep_val]], 
                              columns=['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep'])
    
    # Predict
    predicted_score = model.predict(input_data)[0]
    
    # Evaluate
    grade, risk_level = evaluate_performance(predicted_score)
    recommendations = generate_recommendations(study_hours, attendance, prev_score, test_prep_str)
    
    # Display Results
    st.header("📊 Analysis Results")
    
    # Metrics Row
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Predicted Score", f"{predicted_score:.2f} / 100")
    metric_col2.metric("Expected Grade", grade)
    
    # Color-code risk level
    if risk_level == "Low":
        metric_col3.metric("Risk Level", "🟢 Low")
    elif risk_level == "Medium":
        metric_col3.metric("Risk Level", "🟡 Medium")
    else:
        metric_col3.metric("Risk Level", "🔴 High")
        
    st.subheader("💡 Personalized Recommendations")
    for rec in recommendations:
        st.info(rec)
