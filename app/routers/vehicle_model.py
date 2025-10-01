from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.vehicle_model import VehicleModel, VehicleModelCreate, VehicleModelUpdate
from app.crud.vehicle_model import get_vehicle_model, get_vehicle_models, create_vehicle_model, update_vehicle_model, delete_vehicle_model
from app.core.database import get_db

router = APIRouter(
    prefix="/vehicles_model",
    tags=["vehicles_model"]
)

@router.get("/", response_model=List[VehicleModel])
def read_vehicle_models(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_vehicle_models(db, skip=skip, limit=limit)

@router.post("/", response_model=VehicleModel)
def create_new_vehicle_model(model: VehicleModelCreate, db: Session = Depends(get_db)):
    return create_vehicle_model(db, model)

@router.get("/{model_id}", response_model=VehicleModel)
def read_vehicle_model(model_id: int, db: Session = Depends(get_db)):
    db_model = get_vehicle_model(db, model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Vehicle Model not found")
    return db_model

@router.put("/{model_id}", response_model=VehicleModel)
def update_existing_vehicle_model(model_id: int, model: VehicleModelUpdate, db: Session = Depends(get_db)):
    db_model = update_vehicle_model(db, model_id, model)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Vehicle Model not found")
    return db_model

@router.delete("/{model_id}", response_model=VehicleModel)
def delete_existing_vehicle_model(model_id: int, db: Session = Depends(get_db)):
    db_model = delete_vehicle_model(db, model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Vehicle Model not found")
    return db_model
