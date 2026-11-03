import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import get_db
from app.models.models import Base
from app.services.scoring import calculate_impact_score, get_priority_from_score
from app.services.seed import seed_demo_data

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    seed_demo_data(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_incident():
    response = client.post("/incidents/", json={"category":"Waste Management","description":"Overflowing community bin near park","location":"Jayanagar"})
    assert response.status_code == 200
    assert response.json()["id"]

def test_invalid_incident_input():
    response = client.post("/incidents/", json={"category":"Waste Management","description":"Overflowing bin"})
    assert response.status_code == 422

def test_ai_investigation_workflow():
    response = client.post("/ai/investigate/1")
    assert response.status_code == 200
    assert response.json()["incident"]["ai_assessment"]

def test_update_incident_status():
    response = client.patch("/incidents/1", json={"status":"Resolved"})
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"

def test_duplicate_detection_data():
    rows = client.get("/incidents/1/relationships").json()
    assert any(row["relationship_type"] == "Duplicate" for row in rows)

def test_impact_score_weights_and_priority():
    assert calculate_impact_score(100,100,100,100,100) == 100
    assert calculate_impact_score(0,0,0,0,0) == 0
    assert get_priority_from_score(85) == "Critical"
    assert get_priority_from_score(65) == "High"


def test_add_action_accepts_json_body():
    response = client.post("/incidents/1/actions", json={"action_text":"Inspect and secure the reported pothole","reasoning":"Potential road safety risk near a school."})
    assert response.status_code == 200
    assert response.json()["action_text"].startswith("Inspect")
