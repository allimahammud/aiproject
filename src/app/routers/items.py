from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, models
from ..services.item_service import ItemService
from fastapi.security import OAuth2PasswordBearer
from ..utils import security

router = APIRouter(prefix="/items", tags=["Items"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = security.decode_token(token)
        user_id = int(payload.get("sub"))
        user = db.query(models.User).get(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid user")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=list[schemas.Item])
def list_items(db: Session = Depends(get_db)):
    return ItemService.list_items(db)

@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ItemService.create_item(item, db, owner_id=current_user.id)
