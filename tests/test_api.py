import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Accessibility Focus Assistant API" in data["message"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_process_endpoint_valid_input():
    """Test the process endpoint with valid input"""
    test_input = {
        "text": "You need to prepare a presentation by Friday. Include three main points."
    }
    response = client.post("/process", json=test_input)
    assert response.status_code == 200
    data = response.json()
    
    # Verify all required fields are present
    assert "simplified_text" in data
    assert "audio_narration_script" in data
    assert "visual_task_steps" in data
    assert "action_items" in data
    assert "guided_focus_sessions" in data
    
    # Verify data types
    assert isinstance(data["simplified_text"], str)
    assert isinstance(data["audio_narration_script"], str)
    assert isinstance(data["visual_task_steps"], list)
    assert isinstance(data["action_items"], list)
    assert isinstance(data["guided_focus_sessions"], list)


def test_process_endpoint_empty_input():
    """Test the process endpoint with empty input"""
    test_input = {"text": ""}
    response = client.post("/process", json=test_input)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_process_endpoint_whitespace_only():
    """Test the process endpoint with whitespace only"""
    test_input = {"text": "   "}
    response = client.post("/process", json=test_input)
    assert response.status_code == 400


def test_process_endpoint_long_input():
    """Test the process endpoint with very long input"""
    test_input = {"text": "a" * 15000}
    response = client.post("/process", json=test_input)
    assert response.status_code == 400
    assert "too long" in response.json()["detail"].lower()


def test_action_items_structure():
    """Test that action items have correct structure"""
    test_input = {
        "text": "Complete the report by Monday. Send email to manager."
    }
    response = client.post("/process", json=test_input)
    assert response.status_code == 200
    data = response.json()
    
    action_items = data["action_items"]
    assert len(action_items) > 0
    
    # Check first action item structure
    item = action_items[0]
    assert "task" in item
    assert "owner" in item
    assert "priority" in item
    assert "deadline" in item


def test_focus_sessions_structure():
    """Test that focus sessions have correct structure"""
    test_input = {
        "text": "Prepare presentation with three slides."
    }
    response = client.post("/process", json=test_input)
    assert response.status_code == 200
    data = response.json()
    
    sessions = data["guided_focus_sessions"]
    assert len(sessions) > 0
    
    # Check first session structure
    session = sessions[0]
    assert "session_name" in session
    assert "duration_minutes" in session
    assert "instructions" in session
    assert "break_minutes" in session
    assert isinstance(session["instructions"], list)
