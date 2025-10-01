from sqlalchemy.orm import Session
from app.models.ticket_category import TicketCategory
from app.schemas.ticket_category import TicketCategoryCreate, TicketCategoryUpdate

def get_category(db: Session, category_id: int):
    return db.query(TicketCategory).filter(TicketCategory.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TicketCategory).offset(skip).limit(limit).all()

def create_category(db: Session, category: TicketCategoryCreate):
    db_category = TicketCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: TicketCategoryUpdate):
    db_category = db.query(TicketCategory).filter(TicketCategory.id == category_id).first()
    if db_category:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(TicketCategory).filter(TicketCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
