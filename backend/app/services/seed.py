from sqlalchemy.orm import Session
from ..models.models import (
    Incident,
    IncidentRelationship,
    RecommendedAction,
    SimulatedEnvironmentalReading,
    ActionExecution, IncidentStatusHistory, AgentActivity, ResidentFeedback
)
from datetime import datetime, timedelta

def seed_demo_data(db: Session):
    # Clear existing data to ensure a clean demo
    db.query(ActionExecution).delete()
    db.query(IncidentStatusHistory).delete()
    db.query(AgentActivity).delete()
    db.query(ResidentFeedback).delete()
    db.query(IncidentRelationship).delete()
    db.query(RecommendedAction).delete()
    db.query(Incident).delete()
    db.query(SimulatedEnvironmentalReading).delete()

    # --- SCENARIO A: POTHOLE AND TRAFFIC ---
    # Canonical Pothole Incident
    pothole_main = Incident(
        category="Road Safety / Potholes",
        description="Massive pothole right at the school entrance on 100ft Road, causing cars to swerve into oncoming traffic.",
        location="100ft Road, Indiranagar",
        priority="Critical",
        impact_score=85.0,
        status="Analyzed",
        ai_assessment="Triage: Identified as a critical safety hazard.\nSpecialist: High risk of accident near school zone. Immediate filling required."
    )
    db.add(pothole_main)
    db.commit()

    # Duplicate Pothole Report 1
    pothole_dup1 = Incident(
        category="Road Safety / Potholes",
        description="Huge hole in the road near the school in Indiranagar. Very dangerous!",
        location="100ft Road, Indiranagar",
        status="Reported"
    )
    db.add(pothole_dup1)
    db.commit()

    # Duplicate Pothole Report 2
    pothole_dup2 = Incident(
        category="Road Safety / Potholes",
        description="Pothole at school gate Indiranagar 100ft road",
        location="100ft Road, Indiranagar",
        status="Reported"
    )
    db.add(pothole_dup2)
    db.commit()

    # Related Traffic Incident
    traffic_jam = Incident(
        category="Traffic Congestion",
        description="Severe traffic congestion on 100ft Road near Indiranagar school. Traffic is barely moving.",
        location="100ft Road, Indiranagar",
        priority="Medium",
        impact_score=45.0,
        status="Reported"
    )
    db.add(traffic_jam)
    db.commit()

    # Create Relationships for Scenario A
    db.add(IncidentRelationship(
        source_id=pothole_main.id,
        related_id=pothole_dup1.id,
        relationship_type="Duplicate",
        evidence="Same location and describes the same pothole.",
        is_confirmed=True
    ))
    db.add(IncidentRelationship(
        source_id=pothole_main.id,
        related_id=pothole_dup2.id,
        relationship_type="Duplicate",
        evidence="High similarity in description and location.",
        is_confirmed=True
    ))
    db.add(IncidentRelationship(
        source_id=pothole_main.id,
        related_id=traffic_jam.id,
        relationship_type="Related",
        evidence="The pothole is causing drivers to slow down and swerve, contributing to the congestion.",
        is_confirmed=False
    ))

    # Recommended Action for Pothole
    db.add(RecommendedAction(
        incident_id=pothole_main.id,
        action_text="Deploy emergency road repair crew for cold-mix filling.",
        reasoning="Urgent safety risk at school zone."
    ))
    db.commit()

    # --- SCENARIO B: RAINFALL AND WATERLOGGING ---
    # Environmental Reading: Heavy Rain
    db.add(SimulatedEnvironmentalReading(
        location="Koramangala",
        reading_type="Rainfall",
        value=120.0,
        unit="mm",
        timestamp=datetime.utcnow()
    ))

    # Blocked Drain Incident
    blocked_drain = Incident(
        category="Flood Risk / Drainage",
        description="Drainage grate completely blocked by plastic waste near 80ft road Koramangala.",
        location="80ft Road, Koramangala",
        priority="High",
        impact_score=70.0,
        status="Analyzed",
        ai_assessment="Triage: Drainage blockage identified.\nSpecialist: Critical risk of waterlogging given current heavy rainfall."
    )
    db.add(blocked_drain)
    db.commit()

    # Related Waterlogging Incident
    waterlogging = Incident(
        category="Flood Risk / Drainage",
        description="Road is completely flooded here, cars are stalling.",
        location="80ft Road, Koramangala",
        priority="High",
        impact_score=75.0,
        status="Reported"
    )
    db.add(waterlogging)
    db.commit()

    db.add(IncidentRelationship(
        source_id=blocked_drain.id,
        related_id=waterlogging.id,
        relationship_type="Related",
        evidence="Blocked drain is the likely cause of the observed waterlogging.",
        is_confirmed=False
    ))

    db.add(RecommendedAction(
        incident_id=blocked_drain.id,
        action_text="Urgent desilting of drainage line and waste removal.",
        reasoning="Prevent further flooding and restore road accessibility."
    ))
    db.commit()

    # --- SCENARIO C: WASTE COLLECTION ---
    # Waste Incident 1
    waste1 = Incident(
        category="Waste Management",
        description="Huge pile of garbage overflowing from the community bin.",
        location="HSR Layout Sector 2",
        priority="Medium",
        impact_score=40.0,
        status="Analyzed"
    )
    db.add(waste1)
    db.commit()

    # Waste Incident 2 (Duplicate)
    waste2 = Incident(
        category="Waste Management",
        description="Garbage bin is overflowing, smells terrible.",
        location="HSR Layout Sector 2",
        status="Reported"
    )
    db.add(waste2)
    db.commit()

    # Waste Incident 3 (Nearby)
    waste3 = Incident(
        category="Waste Management",
        description="Waste not collected for 3 days at the corner of the street.",
        location="HSR Layout Sector 2",
        status="Reported"
    )
    db.add(waste3)
    db.commit()

    db.add(IncidentRelationship(source_id=waste1.id, related_id=waste2.id, relationship_type="Duplicate", evidence="Same bin location.", is_confirmed=True))
    db.add(IncidentRelationship(source_id=waste1.id, related_id=waste3.id, relationship_type="Related", evidence="Multiple missed collections in the same sector.", is_confirmed=False))

    db.add(RecommendedAction(
        incident_id=waste1.id,
        action_text="Re-route garbage truck for emergency pickup in HSR Sector 2.",
        reasoning="Multiple reports of overflowing waste indicate a systemic collection failure in this area."
    ))
    db.commit()

    # --- ADDITIONAL EXAMPLES ---
    # Water Conservation
    water_leak = Incident(
        category="Water Conservation",
        description="Major pipe burst on the main road, water gushing out for hours.",
        location="Malleshwaram",
        priority="High",
        impact_score=65.0,
        status="Reported"
    )
    db.add(water_leak)
    db.commit()

    # Road Safety Nudge
    safety_report = Incident(
        category="Road Safety / Potholes",
        description="Lack of pedestrian crossing near the market area, very dangerous for elders.",
        location="Jayanagar",
        priority="Medium",
        impact_score=35.0,
        status="Analyzed"
    )
    db.add(safety_report)
    db.commit()

    db.commit()
