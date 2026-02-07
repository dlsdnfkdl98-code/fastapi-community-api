import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session

from app.config.db import Base, engine, get_db
from app.domain.user import User

app = FastAPI(title="Simple Community API")

# ===== Security settings =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)

JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


# ✅ DB 테이블 생성은 startup에서
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ===== Schemas =====
class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=4, max_length=72)
    nickname: constr(min_length=1, max_length=50)


class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=4, max_length=72)


# ===== Helpers =====
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# ===== Routes =====
@app.get("/")
def root():
    return {"message": "Hello Backend"}


@app.post("/auth/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == req.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        nickname=req.nickname,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "nickname": user.nickname}


@app.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nickname": current_user.nickname,
    }
