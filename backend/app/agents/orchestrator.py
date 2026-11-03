from typing import Dict, Any, List, Optional
from .adapter import get_llm_adapter, AIResponse
from ..db.session import Session
from ..models.models import Incident, IncidentRelationship, RecommendedAction, AgentActivity
from ..services.scoring import calculate_impact_score, get_priority_from_score

class SpecialistAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.adapter = get_llm_adapter()

    def analyze(self, prompt: str) -> AIResponse:
        return self.adapter.generate(prompt, self.system_prompt)

# Specialist Agent Definitions
TRIAGE_AGENT = SpecialistAgent(
    "Civic Triage Agent",
    "You are the primary triage agent for Bengaluru CivicPilot. Your job is to interpret resident complaints, classify them into categories (Traffic, Waste, Water, Flood, Road Safety), and extract key details."
)

ROAD_AGENT = SpecialistAgent(
    "Road Intelligence Agent",
    "You are a road infrastructure expert. Analyze potholes, traffic congestion, and road safety. Recommend alternative routes and safety nudges."
)

WASTE_AGENT = SpecialistAgent(
    "Waste Management Agent",
    "You are a waste management specialist. Handle overflowing bins and missed collections. Group nearby waste incidents and suggest collection plans."
)

WATER_AGENT = SpecialistAgent(
    "Water Conservation Agent",
    "You are a water conservation expert. Analyze leak reports and estimate wastage. Recommend inspection and conservation actions."
)

FLOOD_AGENT = SpecialistAgent(
    "Flood Risk Agent",
    "You are a flood risk specialist. Analyze rainfall and drainage reports. Identify overlapping risk factors and recommend preventive actions."
)

RESOLUTION_AGENT = SpecialistAgent(
    "Resolution and Follow-up Agent",
    "You are a resolution specialist. Track incident status, identify overdue tasks, and generate resident updates."
)

class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.agents = {
            "Triage": TRIAGE_AGENT,
            "Road": ROAD_AGENT,
            "Waste": WASTE_AGENT,
            "Water": WATER_AGENT,
            "Flood": FLOOD_AGENT,
            "Resolution": RESOLUTION_AGENT
        }

    def triage_incident(self, incident_id: int):
        incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return None

        # 1. Triage analysis
        triage_res = self.agents["Triage"].analyze(f"Classify and analyze this {incident.category} complaint at {incident.location}: {incident.description}")

        # 2. Route to specialist
        category = triage_res.structured_data.get("category", "General") if triage_res.structured_data else "General"
        specialist_map = {
            "Road Safety": "Road",
            "Road Safety / Potholes": "Road",
            "Traffic Congestion": "Road",
            "Road Safety Nudges": "Road",
            "Traffic": "Road",
            "Waste Management": "Waste",
            "Water Conservation": "Water",
            "Water Leakage": "Water",
            "Flood Risk": "Flood",
            "Flood Risk / Drainage": "Flood"
        }
        specialist_key = specialist_map.get(category, "Triage")
        specialist_agent = self.agents[specialist_key]

        # 3. Specialist analysis
        specialist_res = specialist_agent.analyze(f"Provide a detailed recommendation for this {category} incident: {incident.description}")

        # 4. Record Activity
        self._log_activity(incident_id, "Triage", triage_res.content)
        self._log_activity(incident_id, specialist_agent.name, specialist_res.content)

        # 5. Update Incident
        incident.ai_assessment = f"Triage: {triage_res.reasoning}\nSpecialist: {specialist_res.reasoning}"

        # 6. Deterministic prototype impact score; LLM output never controls this value.
        safety = 90 if "pothole" in incident.description.lower() or "school" in incident.description.lower() else 55
        people = 70 if "school" in incident.description.lower() or "traffic" in incident.description.lower() else 45
        infrastructure = 75 if any(k in incident.description.lower() for k in ["leak", "drain", "flood", "pothole"]) else 40
        related_count = self.db.query(IncidentRelationship).filter((IncidentRelationship.source_id == incident_id) | (IncidentRelationship.related_id == incident_id)).count()
        incident.impact_score = calculate_impact_score(safety, people, infrastructure, 30, min(100, related_count * 25))
        incident.priority = get_priority_from_score(incident.impact_score)

        # 7. Create Recommended Action
        rec_action = RecommendedAction(
            incident_id=incident_id,
            action_text=specialist_res.content,
            reasoning=specialist_res.reasoning
        )
        self.db.add(rec_action)

        self.db.commit()
        self.db.refresh(incident)
        return incident

    def _log_activity(self, incident_id: int, agent_name: str, log: str):
        activity = AgentActivity(incident_id=incident_id, agent_name=agent_name, activity_log=log)
        self.db.add(activity)
        self.db.commit()
