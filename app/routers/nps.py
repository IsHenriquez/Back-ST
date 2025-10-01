from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.nps import NPS, NPSCreate, NPSUpdate
from app.crud.nps import get_nps, get_all_nps, create_nps, update_nps, delete_nps
from app.core.database import get_db

router = APIRouter(
    prefix="/nps",
    tags=["nps"]
)

@router.get("/", response_model=List[NPS])
def read_nps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_nps(db, skip=skip, limit=limit)

@router.post("/", response_model=NPS)
def create_new_nps(nps: NPSCreate, db: Session = Depends(get_db)):
    return create_nps(db, nps)

@router.get("/{nps_id}", response_model=NPS)
def read_nps_by_id(nps_id: int, db: Session = Depends(get_db)):
    db_nps = get_nps(db, nps_id)
    if db_nps is None:
        raise HTTPException(status_code=404, detail="NPS not found")
    return db_nps

@router.put("/{nps_id}", response_model=NPS)
def update_existing_nps(nps_id: int, nps: NPSUpdate, db: Session = Depends(get_db)):
    db_nps = update_nps(db, nps_id, nps)
    if db_nps is None:
        raise HTTPException(status_code=404, detail="NPS not found")
    return db_nps

@router.delete("/{nps_id}", response_model=NPS)
def delete_existing_nps(nps_id: int, db: Session = Depends(get_db)):
    db_nps = delete_nps(db, nps_id)
    if db_nps is None:
        raise HTTPException(status_code=404, detail="NPS not found")
    return db_nps
