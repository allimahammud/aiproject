from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..database import SessionLocal
from .. import models, schemas
from ..utils import security

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = security.hash_password(user.password)
    u = models.User(email=user.email, password_hash=hashed)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"message": "registered"}

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = security.create_access_token(str(user.id))
    refresh = security.create_refresh_token(str(user.id))
    # include refresh token in response for convenience
    return {"access_token": access, "token_type": "bearer", "refresh_token": refresh}

@router.post("/refresh", response_model=schemas.Token)
def refresh(token: str = Depends(oauth2_scheme)):
    try:
        payload = security.decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        sub = payload.get("sub")
        access = security.create_access_token(sub)
        refresh = security.create_refresh_token(sub)
        return {"access_token": access, "token_type": "bearer", "refresh_token": refresh}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
