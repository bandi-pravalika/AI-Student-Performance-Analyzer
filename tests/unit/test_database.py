"""Unit tests for SQLite database layer."""
import pytest
import os
import sqlite3
from src.core.config import config
from src.core.database import (
    get_db_connection,
    init_db,
    save_prediction,
    get_prediction_history,
    clear_prediction_history
)

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Sets up a temporary SQLite database for unit testing."""
    test_db_path = "test_student_analyzer.db"
    monkeypatch.setattr(config, "DATABASE_PATH", test_db_path)
    
    # Initialize the test database
    init_db()
    
    yield
    
    # Tear down - remove test database file
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except Exception:
            pass

def test_init_db():
    """Verify that tables are created on database initialization."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predictions'")
    table = cursor.fetchone()
    conn.close()
    
    assert table is not None
    assert table["name"] == "predictions"

def test_save_prediction():
    """Test inserting a new prediction into the database."""
    pred_id = save_prediction(
        student_name="Test Student",
        study_hours=8.0,
        attendance=90.0,
        prev_score=85.0,
        test_prep=1,
        predicted_score=88.5,
        grade="A",
        risk_level="Low",
        risk_score=10.0
    )
    
    assert pred_id is not None
    assert pred_id > 0
    
    # Verify values inside database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE id = ?", (pred_id,))
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row["student_name"] == "Test Student"
    assert row["study_hours"] == 8.0
    assert row["attendance"] == 90.0
    assert row["prev_score"] == 85.0
    assert row["predicted_score"] == 88.5
    assert row["grade"] == "A"
    assert row["risk_level"] == "Low"

def test_get_prediction_history():
    """Test fetching historical prediction records."""
    save_prediction(
        student_name="Alice",
        study_hours=4.0,
        attendance=80.0,
        prev_score=70.0,
        test_prep=0,
        predicted_score=72.0,
        grade="B",
        risk_level="Medium",
        risk_score=40.0
    )
    
    save_prediction(
        student_name="Bob",
        study_hours=9.0,
        attendance=95.0,
        prev_score=90.0,
        test_prep=1,
        predicted_score=94.0,
        grade="A",
        risk_level="Low",
        risk_score=5.0
    )
    
    history = get_prediction_history(limit=10)
    
    assert len(history) == 2
    assert history[0]["student_name"] == "Bob"  # Ordered by DESC created_at
    assert history[1]["student_name"] == "Alice"

def test_clear_prediction_history():
    """Test clearing all prediction history logs."""
    save_prediction(
        student_name="Charlie",
        study_hours=5.0,
        attendance=80.0,
        prev_score=75.0,
        test_prep=1,
        predicted_score=78.0,
        grade="B",
        risk_level="Low",
        risk_score=20.0
    )
    
    history_before = get_prediction_history()
    assert len(history_before) == 1
    
    success = clear_prediction_history()
    assert success is True
    
    history_after = get_prediction_history()
    assert len(history_after) == 0
