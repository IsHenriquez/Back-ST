from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.vehicle_brand import VehicleBrand, VehicleBrandCreate, VehicleBrandUpdate
from app.crud.vehicle_brand import get_vehicle_brand, get_vehicle_brands, create_vehicle_brand, update_vehicle_brand, delete_vehicle_brand
from app.core.database import get_db

router = APIRouter(
    prefix="/vehicles_brand",
    tags=["vehicles_brand"]
)

@router.get("/", response_model=List[VehicleBrand])
def read_vehicle_brands(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_vehicle_brands(db, skip=skip, limit=limit)

@router.post("/", response_model=VehicleBrand)
def create_new_vehicle_brand(brand: VehicleBrandCreate, db: Session = Depends(get_db)):
    return create_vehicle_brand(db, brand)

@router.get("/{brand_id}", response_model=VehicleBrand)
def read_vehicle_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = get_vehicle_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Vehicle Brand not found")
    return db_brand

@router.put("/{brand_id}", response_model=VehicleBrand)
def update_existing_vehicle_brand(brand_id: int, brand: VehicleBrandUpdate, db: Session = Depends(get_db)):
    db_brand = update_vehicle_brand(db, brand_id, brand)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Vehicle Brand not found")
    return db_brand

@router.delete("/{brand_id}", response_model=VehicleBrand)
def delete_existing_vehicle_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = delete_vehicle_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Vehicle Brand not found")
    return db_brand
