from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.auth_utils import hash_password, verify_password, create_access_token
from app.auth.auth_utils import oauth2_scheme, token_blacklist

router = APIRouter(prefix="/auth", tags=["Auth"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ✅ LOGIN (OAuth format)
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form.username).first()

    if not db_user or not verify_password(form.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ✅ LOGOUT
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    token_blacklist.add(token)
    return {"message": "Logged out successfully"}

