from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False) # Traffic, Waste, Water, Flood, etc.
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(String, default="Medium") # Low, Medium, High, Critical
    impact_score = Column(Float, default=0.0)
    status = Column(String, default="Reported") # Reported -> Analyzed -> Action Recommended -> Approved -> In Progress -> Resolved
    assigned_department = Column(String, nullable=True)
    ai_assessment = Column(Text, nullable=True)

    # Relationships
    relationships = relationship("IncidentRelationship", back_populates="source_incident", foreign_keys="IncidentRelationship.source_id")
    history = relationship("IncidentStatusHistory", back_populates="incident")
    actions = relationship("RecommendedAction", back_populates="incident")
    feedback = relationship("ResidentFeedback", back_populates="incident")

class IncidentRelationship(Base):
    __tablename__ = "incident_relationships"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("incidents.id"))
    related_id = Column(Integer, ForeignKey("incidents.id"))
    relationship_type = Column(String) # Duplicate, Related, Confirmed
    evidence = Column(Text)
    confidence = Column(Float, nullable=True)
    is_confirmed = Column(Boolean, default=False)

    source_incident = relationship("Incident", foreign_keys=[source_id], back_populates="relationships")

class RecommendedAction(Base):
    __tablename__ = "recommended_actions"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    action_text = Column(Text, nullable=False)
    reasoning = Column(Text)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="actions")

class ActionExecution(Base):
    __tablename__ = "action_executions"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("recommended_actions.id"))
    executed_at = Column(DateTime, default=datetime.utcnow)
    result_log = Column(Text)
    status = Column(String) # Success, Failed

class IncidentStatusHistory(Base):
    __tablename__ = "incident_status_history"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    status = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)
    comment = Column(String)

    incident = relationship("Incident", back_populates="history")

class AgentActivity(Base):
    __tablename__ = "agent_activity"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    agent_name = Column(String)
    activity_log = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ResidentFeedback(Base):
    __tablename__ = "resident_feedback"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    rating = Column(Integer) # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="feedback")

class SimulatedEnvironmentalReading(Base):
    __tablename__ = "environmental_readings"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    reading_type = Column(String) # Rainfall, TrafficLevel, WaterLevel
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
