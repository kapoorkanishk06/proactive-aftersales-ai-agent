# data.py

from datetime import datetime
from typing import List, Dict

# Each "reading" is one vehicle snapshot
MOCK_VEHICLE_DATA: List[Dict] = [
    {
        "vehicle_id": "MH12AB1234",
        "model": "SUV-X",
        "timestamp": "2025-12-02T10:00:00",
        "engine_temp": 88,         # in °C
        "vibration_level": 0.3,    # 0–1
        "error_code": None,
        "mileage_km": 24000,
    },
    {
        "vehicle_id": "MH14CD5678",
        "model": "Hatchback-Z",
        "timestamp": "2025-12-02T10:05:00",
        "engine_temp": 105,
        "vibration_level": 0.7,
        "error_code": "P0420",
        "mileage_km": 52000,
    },
    {
        "vehicle_id": "DL01EF2468",
        "model": "Sedan-Pro",
        "timestamp": "2025-12-02T10:10:00",
        "engine_temp": 95,
        "vibration_level": 0.5,
        "error_code": "P0300",
        "mileage_km": 78000,
    },
]


HIGH_TEMP_THRESHOLD = 100
MEDIUM_TEMP_THRESHOLD = 90
HIGH_VIBRATION_THRESHOLD = 0.7
MEDIUM_VIBRATION_THRESHOLD = 0.4


def compute_risk(vehicle_snapshot: Dict) -> Dict:
    """
    Very simple rule-based risk engine.
    Returns risk_level + reason.
    """
    temp = vehicle_snapshot["engine_temp"]
    vib = vehicle_snapshot["vibration_level"]
    error = vehicle_snapshot["error_code"]

    reasons = []

    # Engine temperature rules
    if temp >= HIGH_TEMP_THRESHOLD:
        reasons.append(f"High engine temperature ({temp}°C)")
        risk_score = 3
    elif temp >= MEDIUM_TEMP_THRESHOLD:
        reasons.append(f"Elevated engine temperature ({temp}°C)")
        risk_score = 2
    else:
        risk_score = 1

    # Vibration rules
    if vib >= HIGH_VIBRATION_THRESHOLD:
        reasons.append(f"High vibration level ({vib})")
        risk_score = max(risk_score, 3)
    elif vib >= MEDIUM_VIBRATION_THRESHOLD:
        reasons.append(f"Moderate vibration level ({vib})")
        risk_score = max(risk_score, 2)

    # Error-code based rules
    if error is not None:
        reasons.append(f"Active fault code: {error}")
        risk_score = max(risk_score, 3)

    # Map numeric score to label
    if risk_score == 3:
        level = "HIGH"
    elif risk_score == 2:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_level": level,
        "reasons": reasons or ["All parameters within normal range."],
    }


def get_latest_snapshot(vehicle_id: str) -> Dict | None:
    """
    Right now each vehicle has only one entry.
    In a real system this would pick the latest timestamp.
    """
    for v in MOCK_VEHICLE_DATA:
        if v["vehicle_id"] == vehicle_id:
            return v
    return None
