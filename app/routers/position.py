from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# ⬅️ Modelo para validar datos de entrada
class PositionCreate(BaseModel):
    id_user: int
    address: str
    latitude: float
    longitude: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# ⬅️ GET - Obtener todas las posiciones
@router.get("/position")
async def get_positions():
    try:
        # Aquí debes conectarte a tu BD y hacer SELECT
        # Ejemplo con tu conexión existente:
        from app.core.database import get_db  # O como tengas tu conexión
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM position ORDER BY updated_at DESC")
        positions = cursor.fetchall()
        
        # Convertir a diccionario
        result = []
        for pos in positions:
            result.append({
                "id": pos[0],
                "id_user": pos[1],
                "address": pos[2],
                "latitude": pos[3],
                "longitude": pos[4],
                "created_at": pos[5],
                "updated_at": pos[6]
            })
        
        return {"success": True, "data": result}
    
    except Exception as e:
        print(f"Error en GET /position: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ⬅️ POST - Crear nueva posición
@router.post("/position")
async def create_position(position: PositionCreate):
    try:
        from app.core.database import get_db
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Usar timestamp actual si no se proporciona
        now = datetime.now().isoformat()
        created_at = position.created_at or now
        updated_at = position.updated_at or now
        
        query = """
            INSERT INTO position (id_user, address, latitude, longitude, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            position.id_user,
            position.address,
            position.latitude,
            position.longitude,
            created_at,
            updated_at
        ))
        
        conn.commit()
        position_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "Posición creada correctamente",
            "data": {"id": position_id, **position.dict()}
        }
    
    except Exception as e:
        print(f"Error en POST /position: {e}")
        raise HTTPException(status_code=500, detail=str(e))
