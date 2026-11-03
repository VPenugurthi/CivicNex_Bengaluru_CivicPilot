from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..agents.orchestrator import AgentOrchestrator
from ..models.models import Incident


router = APIRouter(prefix="/ai", tags=["AI Agents"])

@router.post("/investigate/{incident_id}")
def run_ai_investigation(incident_id: int, db: Session = Depends(get_db)):
    orchestrator = AgentOrchestrator(db)
    result = orchestrator.triage_incident(incident_id)
    if not result:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"status": "success", "incident": result}
