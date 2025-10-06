from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.vehicle_model import VehicleModel

router = APIRouter()

@router.get("/vehicle")
def my_vehicle(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).get(user_id)
    if not u or not u.id_vehicle:
        return None
    v = db.query(Vehicle).get(u.id_vehicle)
    if not v:
        return None
    model = db.query(VehicleModel).get(v.id_vehicle_model) if v.id_vehicle_model else None
    return {
        "plate": v.plate,
        "model": model.name if model else v.description or "",
        "status": "in_use" if v.is_busy else "ok"
    }
