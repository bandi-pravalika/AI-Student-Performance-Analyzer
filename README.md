# AI Student Performance Analyzer 🎓

An end-to-end Machine Learning web application built with Python and Streamlit. This application predicts a student's final exam score based on their study habits and provides personalized, actionable recommendations to improve performance.

## 🚀 Features
- **Score Prediction:** Uses a Random Forest ML model to predict final scores based on Study Hours, Attendance, Previous Scores, and Test Preparation.
- **Grade & Risk Assessment:** Automatically assigns a Grade (A, B, C, Fail) and a Risk Level (Low, Medium, High).
- **Personalized Recommendations:** A rule-based recommendation engine that suggests targeted improvements.
- **Interactive UI:** Built with Streamlit for a clean, user-friendly interface.

## 📁 Project Structure
- `app.py`: The main Streamlit application containing the UI, ML model generation, and recommendation logic.
- `requirements.txt`: List of Python packages required to run the project.
- `README.md`: Documentation for the project.

## 🛠️ How to Run the Application

1. **Prerequisites:** Ensure you have Python installed (Python 3.7+ is recommended).

2. **Navigate to the Project Directory:**
   Open your terminal/command prompt and navigate to the project folder.

3. **Install Dependencies:**
   Run the following command to install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App:**
   Execute the following command to start the application:
   ```bash
   streamlit run app.py
   ```
   
5. **View the App:**
   Your default web browser should automatically open the app. If not, go to the URL provided in the terminal (usually `http://localhost:8501`).

## 🧠 Recommendation Logic
The recommendation engine works on the following principles:
- **Low Study Hours (< 4 hrs):** Suggests increasing study time.
- **Low Attendance (< 75%):** Advises on the importance of attending classes.
- **Low Previous Score (< 60):** Recommends specific revision strategies.
- **No Test Preparation:** Highly recommends taking a test prep course.
- **Good Habits:** Provides positive reinforcement!
