from sqlalchemy.orm import Session
from app.models.vehicle_brand import VehicleBrand
from app.schemas.vehicle_brand import VehicleBrandCreate, VehicleBrandUpdate

def get_vehicle_brand(db: Session, brand_id: int):
    return db.query(VehicleBrand).filter(VehicleBrand.id == brand_id).first()

def get_vehicle_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VehicleBrand).offset(skip).limit(limit).all()

def create_vehicle_brand(db: Session, brand: VehicleBrandCreate):
    db_brand = VehicleBrand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def update_vehicle_brand(db: Session, brand_id: int, brand: VehicleBrandUpdate):
    db_brand = db.query(VehicleBrand).filter(VehicleBrand.id == brand_id).first()
    if db_brand:
        for key, value in brand.dict(exclude_unset=True).items():
            setattr(db_brand, key, value)
        db.commit()
        db.refresh(db_brand)
    return db_brand

def delete_vehicle_brand(db: Session, brand_id: int):
    db_brand = db.query(VehicleBrand).filter(VehicleBrand.id == brand_id).first()
    if db_brand:
        db.delete(db_brand)
        db.commit()
    return db_brand
