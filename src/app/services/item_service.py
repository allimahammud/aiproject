from sqlalchemy.orm import Session
from .. import models, schemas

class ItemService:
    @staticmethod
    def list_items(db: Session):
        return db.query(models.Item).all()

    @staticmethod
    def create_item(item: schemas.ItemCreate, db: Session, owner_id: int | None = None):
        obj = models.Item(**item.dict(), owner_id=owner_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
