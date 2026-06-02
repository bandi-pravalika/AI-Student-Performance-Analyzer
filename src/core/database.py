"""SQLite database management for prediction history."""
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
from src.core.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they do not exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                study_hours REAL NOT NULL,
                attendance REAL NOT NULL,
                prev_score REAL NOT NULL,
                test_prep INTEGER NOT NULL,
                predicted_score REAL NOT NULL,
                grade TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise e

def save_prediction(
    study_hours: float,
    attendance: float,
    prev_score: float,
    test_prep: int,
    predicted_score: float,
    grade: str,
    risk_level: str,
    risk_score: float,
    student_name: Optional[str] = None
) -> int:
    """Save a student prediction to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO predictions (
                student_name, study_hours, attendance, prev_score, test_prep,
                predicted_score, grade, risk_level, risk_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_name or "Anonymous Student",
            study_hours,
            attendance,
            prev_score,
            test_prep,
            predicted_score,
            grade,
            risk_level,
            risk_score
        ))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.info(f"Saved prediction ID {prediction_id} for {student_name}")
        return prediction_id
    except Exception as e:
        logger.error(f"Failed to save prediction: {str(e)}")
        raise e

def get_prediction_history(limit: int = 100) -> List[Dict]:
    """Retrieve prediction logs ordered by creation date desc."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, study_hours, attendance, prev_score, test_prep,
                   predicted_score, grade, risk_level, risk_score, created_at
            FROM predictions
            ORDER BY created_at DESC, id DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row["id"],
                "student_name": row["student_name"],
                "study_hours": row["study_hours"],
                "attendance": row["attendance"],
                "prev_score": row["prev_score"],
                "test_prep": row["test_prep"],
                "predicted_score": row["predicted_score"],
                "grade": row["grade"],
                "risk_level": row["risk_level"],
                "risk_score": row["risk_score"],
                "created_at": row["created_at"]
            })
        return history
    except Exception as e:
        logger.error(f"Failed to fetch prediction history: {str(e)}")
        return []

def clear_prediction_history() -> bool:
    """Clear all records in the predictions table."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()
        logger.info("Cleared all prediction history")
        return True
    except Exception as e:
        logger.error(f"Failed to clear history: {str(e)}")
        return False

# Auto-initialize database on import
init_db()
