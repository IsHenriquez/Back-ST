from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.vehicle import get_vehicles, create_vehicle, update_vehicle, delete_vehicle, get_vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleOut

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=List[VehicleOut])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_vehicles(db, skip=skip, limit=limit)


@router.get("/{vehicle_id}", response_model=VehicleOut)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.post("/", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle_endpoint(payload: VehicleCreate, db: Session = Depends(get_db)):
    vals = payload.model_dump(exclude_unset=True)
    
    # Si viene 0, convertirlo a None para evitar error de foreign key
    if vals.get("id_vehicle_model") == 0:
        vals["id_vehicle_model"] = None
    
    # Recrear el schema con los valores corregidos
    payload_fixed = VehicleCreate(**vals)
    return create_vehicle(db, payload_fixed)


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle_endpoint(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    vals = payload.model_dump(exclude_unset=True)
    
    # Si viene 0, convertirlo a None
    if vals.get("id_vehicle_model") == 0:
        vals["id_vehicle_model"] = None
    
    payload_fixed = VehicleUpdate(**vals)
    vehicle = update_vehicle(db, vehicle_id, payload_fixed)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle_endpoint(vehicle_id: int, db: Session = Depends(get_db)):
    success = delete_vehicle(db, vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None



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

