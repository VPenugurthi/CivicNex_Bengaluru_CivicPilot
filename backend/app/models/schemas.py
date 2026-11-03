from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class IncidentBase(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=8, max_length=2000)
    location: str = Field(min_length=2, max_length=160)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_department: Optional[str] = None
    impact_score: Optional[float] = None

class IncidentResponse(IncidentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    priority: str
    impact_score: float
    status: str
    assigned_department: Optional[str] = None
    ai_assessment: Optional[str] = None


class RelationshipCreate(BaseModel):
    related_id: int
    relationship_type: str
    evidence: str
    confidence: Optional[float] = None

class ActionCreate(BaseModel):
    action_text: str = Field(min_length=3, max_length=2000)
    reasoning: Optional[str] = Field(default=None, max_length=2000)

class ActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    action_text: str
    reasoning: Optional[str] = None
    is_approved: bool
    created_at: datetime

