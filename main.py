from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models import User
from app.security import hash_password
from app.routers import auth, books, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # The first admin is created from Render environment variables.
    if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
        db = SessionLocal()
        try:
            admin_user = db.scalar(select(User).where(User.email == settings.ADMIN_EMAIL))
            if admin_user is None:
                admin_user = User(
                    name="اصلي اډمین",
                    email=settings.ADMIN_EMAIL,
                    password_hash=hash_password(settings.ADMIN_PASSWORD),
                    role="admin",
                )
                db.add(admin_user)
                db.commit()
            elif admin_user.role != "admin":
                admin_user.role = "admin"
                db.commit()
        finally:
            db.close()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="د افغان ډیجیټل کتابتون د کاروونکو، کتابونو او اډمین API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(admin.router)

@app.get("/", tags=["روغتیا"])
def root():
    return {"message": "افغان ډیجیټل کتابتون API فعال دی", "docs": "/docs"}

@app.get("/api/health", tags=["روغتیا"])
def health():
    return {"status": "ok"}
