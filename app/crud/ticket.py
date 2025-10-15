from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from sqlalchemy import inspect, or_, and_
from app.schemas.ticket import TicketCreate, TicketUpdate
import json, urllib.parse, re

def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def create_ticket(db: Session, obj_in: TicketCreate):
    data = obj_in.model_dump(exclude_unset=True)
    # Defaults de negocio si faltan relaciones
    data.setdefault("id_status", 1)     # ej: estado inicial
    data.setdefault("id_priority", 1)   # ej: prioridad baja
    db_obj = Ticket(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        for key, value in ticket.dict(exclude_unset=True).items():
            setattr(db_ticket, key, value)
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket



def get_tickets_with_filter(db: Session, filters: list, skip: int = 0, limit: int = 10):
    query = db.query(Ticket)
    mapper = inspect(Ticket)

    for f in filters:
        op = f.get("operator")
        prop = f.get("property")
        value = f.get("value")

        if prop not in mapper.attrs.keys():
            continue

        column = getattr(Ticket, prop)

        # Nuevo: operador IN
        if op and op.lower() == "in":
            # asegúrate de que value sea lista/tupla
            if not isinstance(value, (list, tuple, set)):
                value = [value]
            # casteo básico según tipo de columna
            pytype = mapper.columns[prop].type.python_type
            casted = []
            for v in value:
                try:
                    casted.append(pytype(v))
                except Exception:
                    casted.append(v)
            query = query.filter(column.in_(casted))
            continue

        # Resto operadores (=, !=, >, <)
        # Convertir valor al tipo correcto para operadores escalares
        col_type = mapper.columns[prop].type.python_type
        try:
            if col_type == bool:
                if isinstance(value, str):
                    value = value.lower() in ("true", "1", "t")
                else:
                    value = bool(value)
            else:
                value = col_type(value)
        except Exception:
            pass

        if op == "=":
            query = query.filter(column == value)
        elif op == "!=":
            query = query.filter(column != value)
        elif op == ">":
            query = query.filter(column > value)
        elif op == "<":
            query = query.filter(column < value)

    return query.offset(skip).limit(limit).all()


def parse_filter_param(raw: str):
    # 1) Si viene vacío o null
    if raw is None or raw == "":
        return []

    candidates = []

    # Original
    candidates.append(raw)

    # Unquote una vez
    try:
        candidates.append(urllib.parse.unquote(raw))
    except Exception:
        pass

    # Unquote dos veces (algunos clientes doble-encodean)
    try:
        candidates.append(urllib.parse.unquote(urllib.parse.unquote(raw)))
    except Exception:
        pass

    # Reemplazo de comillas simples por dobles
    for s in list(candidates):
        if "'" in s and '"' not in s:
            candidates.append(s.replace("'", '"'))

    # Quitar un trailing apostrophe o comilla perdida al final
    candidates = [re.sub(r"[\"']$", "", s.strip()) for s in candidates]

    # Quitar envolturas tipo filter=... si el cliente pasó todo el query como string
    candidates = [re.sub(r"^filter=", "", s, flags=re.I) for s in candidates]

    # Intentar parsear como JSON lista
    for s in candidates:
        try:
            data = json.loads(s)
            if isinstance(data, list):
                return data
        except Exception:
            continue

    return None