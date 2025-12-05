# main.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict

from data import MOCK_VEHICLE_DATA, compute_risk, get_latest_snapshot

app = FastAPI(title="Proactive Automotive Aftersales – Demo")

# Simple in-memory “database” for bookings
BOOKINGS: List[Dict] = []


class ServiceBookingRequest(BaseModel):
    vehicle_id: str
    preferred_date: str
    preferred_slot: str
    contact_number: str


@app.get("/")
async def root():
    # Serve frontend
    return FileResponse("static/index.html")


@app.get("/api/vehicles")
async def list_vehicles():
    """
    Return all vehicles with current risk level.
    """
    result = []
    for v in MOCK_VEHICLE_DATA:
        risk = compute_risk(v)
        result.append(
            {
                "vehicle_id": v["vehicle_id"],
                "model": v["model"],
                "engine_temp": v["engine_temp"],
                "vibration_level": v["vibration_level"],
                "error_code": v["error_code"],
                "risk_level": risk["risk_level"],
            }
        )
    return {"vehicles": result}


@app.get("/api/vehicles/{vehicle_id}")
async def vehicle_details(vehicle_id: str):
    v = get_latest_snapshot(vehicle_id)
    if v is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    risk = compute_risk(v)
    return {
        "vehicle": v,
        "risk": risk,
    }


@app.post("/api/book-service")
async def book_service(req: ServiceBookingRequest):
    v = get_latest_snapshot(req.vehicle_id)
    if v is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    booking = {
        "vehicle_id": req.vehicle_id,
        "model": v["model"],
        "preferred_date": req.preferred_date,
        "preferred_slot": req.preferred_slot,
        "contact_number": req.contact_number,
        "risk_level": compute_risk(v)["risk_level"],
    }
    BOOKINGS.append(booking)

    # This message simulates the proactive voice/call agent.
    confirmation_message = (
        f"Proactive agent has scheduled a service for vehicle {req.vehicle_id} "
        f"on {req.preferred_date} ({req.preferred_slot}). "
        f"Our service center will contact {req.contact_number} for confirmation."
    )

    return {"status": "success", "booking": booking, "message": confirmation_message}


@app.get("/api/bookings")
async def list_bookings():
    return {"bookings": BOOKINGS}
