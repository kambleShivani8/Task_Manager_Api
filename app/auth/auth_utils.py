from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer



# 🔐 JWT settings
SECRET_KEY = "padma@123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# logout blacklist
token_blacklist = set()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")



# ✅ Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str):
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Protected route dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token is logged out")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
