def calculate_impact_score(
    safety_score: float,
    people_affected_score: float,
    infra_impact_score: float,
    time_unresolved_score: float,
    related_incident_score: float
) -> float:
    """
    Deterministic Impact Score Calculation
    Weights:
    - Safety risk: 35%
    - People affected: 25%
    - Infrastructure impact: 20%
    - Time unresolved: 10%
    - Related incident impact: 10%
    """
    score = (
        (safety_score * 0.35) +
        (people_affected_score * 0.25) +
        (infra_impact_score * 0.20) +
        (time_unresolved_score * 0.10) +
        (related_incident_score * 0.10)
    )
    return round(score, 2)

def get_priority_from_score(score: float) -> str:
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"
