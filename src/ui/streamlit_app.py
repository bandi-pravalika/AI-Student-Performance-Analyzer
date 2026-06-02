"""Premium AI Student Performance Analyzer Streamlit application."""
import streamlit as st
import requests
import pandas as pd
import json
import io
from typing import Dict, List, Optional

# Page configuration for a professional look and feel
st.set_page_config(
    page_title="AI Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Custom Premium Styling & Glassmorphism Design
st.markdown("""
    <style>
    /* Premium fonts and background colors */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }
    
    /* Title and header formatting */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics panel glassmorphism box */
    .metric-container {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
        transition: transform 0.2s ease-in-out;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    /* Custom buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("🎓 AI Student Performance Analyzer")

# Sidebar System Health
with st.sidebar:
    st.image("https://img.icons8.com/color/96/student-male.png", width=70)
    st.header("⚙️ System Hub")
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if health_response.status_code == 200:
            st.success("🟢 API Connected Successfully")
        else:
            st.error("🔴 API Status Error")
    except Exception:
        st.error("❌ API Offline - Please run backend server")
        st.code("python main.py", language="bash")
        st.stop()

# Setup Tabs
tab1, tab2, tab3 = st.tabs([
    "🔮 Single Student Analysis", 
    "📁 Batch CSV Predictor", 
    "📊 Analytics Dashboard & Logs"
])

# -----------------
# TAB 1: Single Prediction
# -----------------
with tab1:
    if "prediction_result" in st.session_state:
        res = st.session_state.prediction_result
        inputs = st.session_state.prediction_inputs
        
        # Navigation header
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("👈 New Analysis", use_container_width=True):
                del st.session_state.prediction_result
                del st.session_state.prediction_inputs
                st.rerun()
        with col_title:
            st.markdown(f"### 📊 Analysis Report for: **{res.get('student_name', 'Anonymous Student')}**")
            
        st.divider()
        
        # Sub-tabs for clean structuring
        sub_tab_metrics, sub_tab_explain, sub_tab_guidance = st.tabs([
            "📊 Core Metrics & Risk Indicators",
            "🧠 AI Model Explanations (SHAP)",
            "💡 Actionable Guidance & Actions"
        ])
        
        with sub_tab_metrics:
            # Render high-level cards
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            risk_color = "🟢" if res['risk_level'] == "Low" else "🟡" if res['risk_level'] == "Medium" else "🔴"
            
            with m_col1:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-size: 14px; color: #94a3b8;">Predicted Final Score</div>
                    <div style="font-size: 28px; font-weight: 700; color: #38bdf8;">{res['predicted_score']:.2f}%</div>
                    <div style="font-size: 12px; color: #64748b;">Confidence interval below</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col2:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-size: 14px; color: #94a3b8;">Expected Grade</div>
                    <div style="font-size: 28px; font-weight: 700; color: #10b981;">Grade {res['grade']}</div>
                    <div style="font-size: 12px; color: #64748b;">Scale: A / B / C / F</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col3:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-size: 14px; color: #94a3b8;">Composite Risk Level</div>
                    <div style="font-size: 28px; font-weight: 700; color: #f59e0b;">{risk_color} {res['risk_level']}</div>
                    <div style="font-size: 12px; color: #64748b;">Based on attendance & study</div>
                </div>
                """, unsafe_allow_html=True)
                
            with m_col4:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-size: 14px; color: #94a3b8;">Composite Risk Score</div>
                    <div style="font-size: 28px; font-weight: 700; color: #ef4444;">{res['risk_score']:.1f} / 100</div>
                    <div style="font-size: 12px; color: #64748b;">Critical threshold: >55%</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.divider()
            
            # Detailed charts and explanation
            left_col, right_col = st.columns([1, 1])
            with left_col:
                st.subheader("🎯 Suggestions for Improving Grades")
                
                # Derive custom grade improvement suggestions
                suggestions = []
                if inputs['study_hours'] < 6.0:
                    suggestions.append("⏰ **Increase Study Focus**: Elevating study time by just 1.5 to 2 hours per week is estimated to boost your final score by 5-8%.")
                if inputs['attendance'] < 85.0:
                    suggestions.append("🏫 **Target 90%+ Attendance**: Attending more lectures provides direct concept continuity. Every 5% increase in attendance reduces grade risks significantly.")
                if inputs['test_prep'] == 0:
                    suggestions.append("📝 **Enroll in Test Prep**: Completing a structured preparation module or mock test can raise performance averages by up to 5 points.")
                if inputs['prev_score'] < 75.0:
                    suggestions.append("📚 **Address Foundational Gaps**: Focus the first 30 minutes of study sessions on reviewing previous weak topics and clarifying doubts with mentors.")
                
                # Default general suggestion
                if not suggestions:
                    suggestions.append("🚀 **Maintain Academic Momentum**: Your habits are exemplary. Focus on teaching concepts to peers (Feynman Technique) to solidify mastery!")
                else:
                    suggestions.append("🔄 **Utilize Spaced Repetition**: Review key formulas and lecture notes 1 day, 3 days, and 7 days after class to maximize memory retention.")
                    
                for sug in suggestions:
                    st.markdown(sug)
                
            with right_col:
                st.subheader("💡 Behavioral Indicators")
                st.markdown(f"""
                - **Low Attendance Risk:** {'🔴 Triggered' if inputs['attendance'] < 75.0 else '🟢 Safe'}
                - **Low Study Hours Risk:** {'🔴 Triggered' if inputs['study_hours'] < 4.0 else '🟢 Safe'}
                - **Prior Score Risk Warning:** {'🔴 Triggered' if inputs['prev_score'] < 60.0 else '🟢 Safe'}
                - **Risk Score Warning:** {'🔴 At Risk' if res['risk_score'] > 55.0 else '🟢 Low Risk'}
                """)
                
        with sub_tab_explain:
            left_col_exp, right_col_exp = st.columns([1, 1])
            with left_col_exp:
                st.subheader("⚡ Ensemble Feature Importance")
                imp_df = pd.DataFrame(
                    list(res['feature_importance'].items()),
                    columns=["Feature", "Relative Importance"]
                ).sort_values("Relative Importance", ascending=True)
                st.bar_chart(imp_df.set_index("Feature"), color="#38bdf8", horizontal=True)
                
            with right_col_exp:
                st.subheader("🧠 Explainable AI: Feature Influence (SHAP-like)")
                shap = res['shap_explanation']
                st.markdown(f"**Calculated baseline prediction (Average Student):** `{shap['base_value']:.1f}%` ➔ **Target Prediction:** `{res['predicted_score']:.1f}%`")
                
                shap_list = []
                for k, v in shap['feature_values'].items():
                    shap_list.append({
                        "Feature Attribute": k,
                        "Observed Value": v['value'],
                        "Impact Direction": "➕ Pos" if v['contribution'] >= 0 else "➖ Neg",
                        "Raw Contribution (Points change)": f"{v['contribution']:+.2f}"
                    })
                st.dataframe(pd.DataFrame(shap_list), use_container_width=True, hide_index=True)
                
        with sub_tab_guidance:
            rec_col, int_col = st.columns(2)
            with rec_col:
                st.subheader("💡 Personalized Recommendations")
                for idx, rec in enumerate(res['recommendations']):
                    p_color = "🔴" if rec['priority'] == 'urgent' else "🟠" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                    with st.expander(f"{p_color} {rec['title']} (Priority: {rec['priority'].upper()})", expanded=(idx == 0)):
                        st.write(f"**Description:** {rec['description']}")
                        st.write(f"👉 **Suggestion:** {rec['suggestion']}")
                        st.write(f"📈 **Expected Impact:** {rec['impact']}")
                        st.write("**Action Plan Checklist:**")
                        for action in rec['action_items']:
                            st.write(f"- [ ] {action}")
                            
            with int_col:
                st.subheader("🆘 Suggested Interventions")
                if res['intervention_actions']:
                    for action in res['intervention_actions']:
                        priority_color = "🔴" if action['priority'] == 'urgent' else "🟠" if action['priority'] == 'high' else "🟡"
                        with st.expander(f"{priority_color} Action: {action['action']}", expanded=True):
                            st.write(f"**Scope:** {action['priority'].upper()}")
                            st.write(f"**Context / Reason:** {action['reason']}")
                else:
                    st.success("🎉 No active educational interventions required at this risk score. Suggest standard monitoring.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👈 Back to Top & Enter New Profile", key="bottom_back_btn", use_container_width=True):
            del st.session_state.prediction_result
            del st.session_state.prediction_inputs
            st.rerun()

    else:
        st.subheader("📋 Enter Student Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("👤 Student Name", value="Alice Smith", placeholder="Enter student's name")
            study_hours = st.slider(
                "📚 Weekly Study Hours",
                min_value=0.0,
                max_value=15.0,
                value=6.0,
                step=0.5,
                help="Number of dedicated hours student studies per week"
            )
            attendance = st.slider(
                "🏫 Attendance Percentage (%)",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=1.0,
                help="Current class attendance rate"
            )
            
        with col2:
            prev_score = st.number_input(
                "📊 Previous Exam Score (0-100)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=1.0,
                help="Score obtained in the prior midterm or exam"
            )
            test_prep = st.selectbox(
                "📝 Completed Test Prep Course?",
                options=["No", "Yes"],
                index=1,
                help="Whether the student completed a preparatory curriculum"
            )
            test_prep_val = 1 if test_prep == "Yes" else 0

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔮 Predict Performance & Generate Recommendations", use_container_width=True):
            with st.spinner("Crunching ensemble models, executing feature pipelines, and deriving SHAP explanations..."):
                try:
                    # Call prediction endpoint
                    response = requests.post(
                        f"{API_BASE_URL}/predictions",
                        json={
                            "student_name": student_name,
                            "Study_Hours": float(study_hours),
                            "Attendance": float(attendance),
                            "Prev_Score": float(prev_score),
                            "Test_Prep": int(test_prep_val)
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.session_state.prediction_result = response.json()
                        st.session_state.prediction_inputs = {
                            "student_name": student_name,
                            "study_hours": float(study_hours),
                            "attendance": float(attendance),
                            "prev_score": float(prev_score),
                            "test_prep": int(test_prep_val)
                        }
                        st.rerun()
                    else:
                        st.error(f"Prediction Service Error: {response.text}")
                except Exception as e:
                    st.error(f"Network / Process Failure: {str(e)}")

# -----------------
# TAB 2: Batch CSV Upload
# -----------------
with tab2:
    st.subheader("📁 Bulk Performance Predictor")
    st.write("Upload a CSV file containing columns for multiple students to make predictions simultaneously. Results are automatically saved to history.")
    
    # Template download
    template_df = pd.DataFrame({
        "student_name": ["Alice Jenkins", "Bob Vance", "Charlie Day"],
        "Study_Hours": [7.5, 3.0, 5.5],
        "Attendance": [95.0, 68.0, 80.0],
        "Prev_Score": [88.0, 52.0, 72.0],
        "Test_Prep": [1, 0, 1]
    })
    
    buffer = io.BytesIO()
    template_df.to_csv(buffer, index=False)
    st.download_button(
        label="📥 Download Template CSV Schema",
        data=buffer.getvalue(),
        file_name="student_prediction_template.csv",
        mime="text/csv"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Select Student CSV File", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("📄 **Raw Upload Preview:**")
            st.dataframe(df.head(), use_container_width=True)
            
            # Check columns
            req_cols = ["Study_Hours", "Attendance", "Prev_Score", "Test_Prep"]
            missing_cols = [c for c in req_cols if c not in df.columns]
            
            if missing_cols:
                st.error(f"Invalid Schema! Missing columns: {missing_cols}")
            else:
                if st.button("🚀 Execute Batch Prediction", type="primary", use_container_width=True):
                    with st.spinner("Processing batch records through ML classifier..."):
                        # Construct payload list
                        payload = []
                        for _, row in df.iterrows():
                            # Optional name
                            s_name = str(row["student_name"]) if "student_name" in df.columns and pd.notna(row["student_name"]) else "Anonymous Student"
                            payload.append({
                                "student_name": s_name,
                                "Study_Hours": float(row["Study_Hours"]),
                                "Attendance": float(row["Attendance"]),
                                "Prev_Score": float(row["Prev_Score"]),
                                "Test_Prep": int(row["Test_Prep"])
                            })
                            
                        # Make request
                        batch_res = requests.post(f"{API_BASE_URL}/batch-predictions", json=payload, timeout=20)
                        
                        if batch_res.status_code == 200:
                            predictions = batch_res.json()["predictions"]
                            
                            # Build output dataset
                            out_rows = []
                            for idx, pred in enumerate(predictions):
                                if "error" in pred:
                                    out_rows.append({
                                        "student_name": payload[idx]["student_name"],
                                        "Error": pred["error"]
                                    })
                                else:
                                    out_rows.append({
                                        "student_name": pred.get("student_name", payload[idx]["student_name"]),
                                        "Predicted Score": f"{pred['predicted_score']:.2f}%",
                                        "Grade": pred["grade"],
                                        "Risk Level": pred["risk_level"],
                                        "Risk Score": f"{pred['risk_score']:.1f}%"
                                    })
                                    
                            out_df = pd.DataFrame(out_rows)
                            st.divider()
                            st.success("🎉 Batch Prediction Completed successfully!")
                            st.dataframe(out_df, use_container_width=True)
                            
                            # Download predictions
                            csv_out_buf = io.BytesIO()
                            out_df.to_csv(csv_out_buf, index=False)
                            st.download_button(
                                label="📥 Export predictions CSV",
                                data=csv_out_buf.getvalue(),
                                file_name="student_prediction_results.csv",
                                mime="text/csv"
                            )
                        else:
                            st.error(f"API Error: {batch_res.text}")
        except Exception as csv_err:
            st.error(f"Error parsing uploaded file: {str(csv_err)}")

# -----------------
# TAB 3: Analytics Dashboard & Logs
# -----------------
with tab3:
    st.subheader("📊 Historical Analytics & Prediction Logs")
    
    # Reload trigger
    if st.button("🔄 Refresh Data logs", use_container_width=True):
        st.toast("Logs updated!")
        
    try:
        hist_res = requests.get(f"{API_BASE_URL}/history?limit=200", timeout=5)
        if hist_res.status_code == 200:
            history = hist_res.json()
            
            if not history:
                st.info("ℹ️ No predictions have been recorded yet. Complete a prediction in Tab 1 or Tab 2 to view statistics.")
            else:
                hist_df = pd.DataFrame(history)
                
                # Render statistics overview cards
                total_records = len(hist_df)
                avg_score = hist_df["predicted_score"].mean()
                at_risk_count = len(hist_df[hist_df["risk_level"] == "High"])
                risk_pct = (at_risk_count / total_records) * 100 if total_records > 0 else 0
                
                st.divider()
                
                # Display metrics layout
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                
                with stats_col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 14px; color: #94a3b8;">Total Records Logged</div>
                        <div style="font-size: 32px; font-weight: 700; color: #38bdf8;">{total_records}</div>
                        <div style="font-size: 12px; color: #64748b;">All-time transactions</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with stats_col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 14px; color: #94a3b8;">Average Predicted Score</div>
                        <div style="font-size: 32px; font-weight: 700; color: #10b981;">{avg_score:.2f}%</div>
                        <div style="font-size: 12px; color: #64748b;">Overall student mean</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with stats_col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 14px; color: #94a3b8;">High-Risk Count</div>
                        <div style="font-size: 32px; font-weight: 700; color: #f59e0b;">{at_risk_count} Students</div>
                        <div style="font-size: 12px; color: #64748b;">Requires immediate support</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with stats_col4:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 14px; color: #94a3b8;">High-Risk Percentage</div>
                        <div style="font-size: 32px; font-weight: 700; color: #ef4444;">{risk_pct:.1f}%</div>
                        <div style="font-size: 12px; color: #64748b;">Proportion of at-risk group</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Visual charts
                st.markdown("<br>", unsafe_allow_html=True)
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.subheader("📊 Grade Distribution")
                    grade_counts = hist_df["grade"].value_counts().reset_index()
                    grade_counts.columns = ["Grade", "Count"]
                    st.bar_chart(grade_counts.set_index("Grade"), color="#10b981")
                    
                with chart_col2:
                    st.subheader("📚 Study Hours vs Predicted Performance")
                    st.scatter_chart(
                        hist_df,
                        x="study_hours",
                        y="predicted_score",
                        color="risk_level"
                    )
                
                # Filters
                st.divider()
                st.subheader("🔍 Prediction Records List")
                
                # Name search filter
                search_q = st.text_input("🔍 Search by Student Name")
                risk_sel = st.selectbox("Filter by Risk Level", options=["All", "Low", "Medium", "High"])
                
                filtered_df = hist_df.copy()
                if search_q:
                    filtered_df = filtered_df[filtered_df["student_name"].str.contains(search_q, case=False, na=False)]
                if risk_sel != "All":
                    filtered_df = filtered_df[filtered_df["risk_level"] == risk_sel]
                
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                
                # Download full history
                hist_csv_buf = io.BytesIO()
                filtered_df.to_csv(hist_csv_buf, index=False)
                st.download_button(
                    label="📥 Export Filtered History (CSV)",
                    data=hist_csv_buf.getvalue(),
                    file_name="student_prediction_history.csv",
                    mime="text/csv"
                )
                
                st.divider()
                st.subheader("🗑️ Database Actions")
                
                clear_confirm = st.checkbox("⚠️ Confirm deletion of entire history log", value=False)
                if clear_confirm:
                    if st.button("🚨 Clear All Prediction Records", type="secondary"):
                        clear_req = requests.delete(f"{API_BASE_URL}/history")
                        if clear_req.status_code == 200:
                            st.success("Prediction logs cleared! Please refresh data logs.")
                        else:
                            st.error(f"Failed to clear history: {clear_req.text}")
        else:
            st.error("Failed to retrieve system prediction logs")
    except Exception as fetch_err:
        st.error(f"Failed to communicate with DB API server: {str(fetch_err)}")
