# app/routers/technician.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.position import Position

router = APIRouter(prefix="/technicians", tags=["technicians"])


# Modelo para validar datos de entrada desde el Mobile
class TechnicianLocationPayload(BaseModel):
    user_id: int
    lat: float
    lng: float


@router.post("/location")
async def update_technician_location(
    payload: TechnicianLocationPayload,
    db: Session = Depends(get_db)
):
    """
    Endpoint llamado desde la app móvil para actualizar la ubicación del técnico.
    
    Recibe:
    - user_id: ID del usuario/técnico
    - lat: Latitud (latitude)
    - lng: Longitud (longitude)
    
    Guarda en la tabla positions con address NULL (puede agregarse geocodificación inversa después).
    """
    try:
        # Crear nueva posición en la base de datos
        new_position = Position(
            id_user=payload.user_id,
            address=None,  
            latitude=payload.lat,
            longitude=payload.lng,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_position)
        db.commit()
        db.refresh(new_position)
        
        return {
            "success": True,
            "message": "Ubicación del técnico actualizada correctamente",
            "data": {
                "id": new_position.id,
                "user_id": new_position.id_user,
                "lat": new_position.latitude,
                "lng": new_position.longitude,
                "updated_at": new_position.updated_at.isoformat()
            }
        }
    
    except Exception as e:
        db.rollback()
        print(f"Error en POST /technicians/location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/{user_id}")
async def get_technician_location(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para que el Dashboard obtenga la última ubicación de un técnico.
    
    Devuelve la posición más reciente del técnico especificado.
    """
    try:
        # Buscar la última posición del técnico
        last_position = db.query(Position).filter(
            Position.id_user == user_id
        ).order_by(Position.updated_at.desc()).first()
        
        if not last_position:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró ubicación para el técnico con user_id={user_id}"
            )
        
        return {
            "success": True,
            "data": {
                "user_id": last_position.id_user,
                "lat": last_position.latitude,
                "lng": last_position.longitude,
                "address": last_position.address,
                "last_update": last_position.updated_at.isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en GET /technicians/location/{user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations")
async def get_all_technicians_locations(db: Session = Depends(get_db)):
    """
    Endpoint para obtener las últimas ubicaciones de TODOS los técnicos.
    Útil para el Dashboard que quiere mostrar todos los técnicos en el mapa.
    
    Devuelve la última posición de cada técnico.
    """
    try:
        # Query para obtener la última posición de cada usuario
        # Usando subquery para obtener el max(updated_at) por usuario
        from sqlalchemy import func
        
        subquery = db.query(
            Position.id_user,
            func.max(Position.updated_at).label('max_updated')
        ).group_by(Position.id_user).subquery()
        
        latest_positions = db.query(Position).join(
            subquery,
            (Position.id_user == subquery.c.id_user) & 
            (Position.updated_at == subquery.c.max_updated)
        ).all()
        
        result = []
        for pos in latest_positions:
            result.append({
                "user_id": pos.id_user,
                "lat": pos.latitude,
                "lng": pos.longitude,
                "address": pos.address,
                "last_update": pos.updated_at.isoformat()
            })
        
        return {
            "success": True,
            "count": len(result),
            "data": result
        }
    
    except Exception as e:
        print(f"Error en GET /technicians/locations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
