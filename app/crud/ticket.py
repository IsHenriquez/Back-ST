from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from sqlalchemy import inspect
from app.schemas.ticket import TicketCreate, TicketUpdate

def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def create_ticket(db: Session, ticket: TicketCreate):
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

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

        # Validar que la propiedad exista en el modelo
        if prop not in mapper.attrs.keys():
            continue

        # Obtener tipo de columna para convertir valor
        col_type = mapper.columns[prop].type.python_type

        # Convertir el valor al tipo correcto (maneja int, float, bool, str)
        try:
            if col_type == bool:
                # Convierte valores tipo bool comunes
                if isinstance(value, str):
                    value = value.lower() in ("true", "1", "t")
                else:
                    value = bool(value)
            else:
                value = col_type(value)
        except Exception:
            # Si no puede convertir, mantener el valor original
            pass

        # Aplicar filtro según operador
        column = getattr(Ticket, prop)

        if op == "=":
            query = query.filter(column == value)
        elif op == "!=":
            query = query.filter(column != value)
        elif op == ">":
            query = query.filter(column > value)
        elif op == "<":
            query = query.filter(column < value)
        # Agregar otros operadores si necesitás

    return query.offset(skip).limit(limit).all()
