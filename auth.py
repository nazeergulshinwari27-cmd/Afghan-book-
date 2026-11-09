from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterInput, LoginInput, AuthResponse, AuthUser
from app.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["حسابونه"])

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(data: RegisterInput, db: Session = Depends(get_db)):
    email = str(data.email).lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=409, detail="دا برېښنالیک مخکې ثبت شوی دی.")
    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthResponse(
        access_token=create_access_token(user),
        user=AuthUser(id=user.id, name=user.name, email=user.email, role=user.role),
    )

@router.post("/login", response_model=AuthResponse)
def login(data: LoginInput, db: Session = Depends(get_db)):
    email = str(data.email).lower()
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="برېښنالیک یا پټ نوم ناسم دی.")
    return AuthResponse(
        access_token=create_access_token(user),
        user=AuthUser(id=user.id, name=user.name, email=user.email, role=user.role),
    )

@router.get("/me", response_model=AuthUser)
def my_account(user: User = Depends(get_current_user)):
    return AuthUser(id=user.id, name=user.name, email=user.email, role=user.role)
