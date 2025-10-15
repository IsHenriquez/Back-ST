from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from app.crud.vehicle import get_vehicle, get_vehicles, create_vehicle, update_vehicle, delete_vehicle
from app.core.database import get_db

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"]
)

@router.get("/", response_model=List[Vehicle])
def read_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_vehicles(db, skip=skip, limit=limit)

@router.post("/", response_model=Vehicle)
def create_new_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    return create_vehicle(db, vehicle)

@router.get("/{vehicle_id}", response_model=Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.put("/{vehicle_id}", response_model=Vehicle)
def update_existing_vehicle(vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    db_vehicle = update_vehicle(db, vehicle_id, vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.delete("/{vehicle_id}", response_model=Vehicle)
def delete_existing_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = delete_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@router.get("/assigned")
def vehicle_assigned(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    # ajusta JOIN según tu modelo/relación
    v = (
        db.query(Vehicle)
        .join(UserVehicle, UserVehicle.vehicle_id == Vehicle.id)
        .filter(UserVehicle.user_id == user_id, UserVehicle.is_active == True)
        .first()
    )
    if not v: return None
    return {"plate": v.plate, "model": v.model, "status": v.status or "unknown"}

