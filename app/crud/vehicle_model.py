from sqlalchemy.orm import Session
from app.models.vehicle_model import VehicleModel
from app.schemas.vehicle_model import VehicleModelCreate, VehicleModelUpdate

def get_vehicle_model(db: Session, model_id: int):
    return db.query(VehicleModel).filter(VehicleModel.id == model_id).first()

def get_vehicle_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VehicleModel).offset(skip).limit(limit).all()

def create_vehicle_model(db: Session, model: VehicleModelCreate):
    db_model = VehicleModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def update_vehicle_model(db: Session, model_id: int, model: VehicleModelUpdate):
    db_model = db.query(VehicleModel).filter(VehicleModel.id == model_id).first()
    if db_model:
        for key, value in model.dict(exclude_unset=True).items():
            setattr(db_model, key, value)
        db.commit()
        db.refresh(db_model)
    return db_model

def delete_vehicle_model(db: Session, model_id: int):
    db_model = db.query(VehicleModel).filter(VehicleModel.id == model_id).first()
    if db_model:
        db.delete(db_model)
        db.commit()
    return db_model
