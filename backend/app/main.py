from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .db.session import get_db, init_db
from .models.models import Incident, IncidentRelationship, RecommendedAction
from .models.schemas import IncidentCreate, IncidentResponse, IncidentUpdate, RelationshipCreate, ActionCreate, ActionResponse
from .api import ai_routes, demo_routes

app = FastAPI(title="Bengaluru CivicPilot API", description="CivicNex · Detect. Connect. Act. Transform.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(ai_routes.router)
app.include_router(demo_routes.router)

@app.on_event("startup")
def on_startup():
    init_db()



@app.get("/")
def read_root():
    return {"message": "Welcome to Bengaluru CivicPilot API"}

@app.post("/incidents/", response_model=IncidentResponse)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    db_incident = Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.get("/incidents/", response_model=List[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@app.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident

@app.patch("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, incident_update: IncidentUpdate, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    for key, value in incident_update.model_dump(exclude_unset=True).items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.get("/incidents/{incident_id}/relationships")
def get_relationships(incident_id: int, db: Session = Depends(get_db)):
    return db.query(IncidentRelationship).filter(
        (IncidentRelationship.source_id == incident_id) |
        (IncidentRelationship.related_id == incident_id)
    ).all()

@app.post("/incidents/{incident_id}/actions", response_model=ActionResponse)
def add_recommended_action(incident_id: int, action: ActionCreate, db: Session = Depends(get_db)):
    if not db.query(Incident).filter(Incident.id == incident_id).first():
        raise HTTPException(status_code=404, detail="Incident not found")
    db_action = RecommendedAction(incident_id=incident_id, action_text=action.action_text, reasoning=action.reasoning)
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action
