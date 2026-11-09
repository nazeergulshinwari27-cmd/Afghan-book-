from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book, User
from app.schemas import BookPublic, UserPublic
from app.security import get_current_admin
from app.routers.books import to_public

router = APIRouter(prefix="/api/admin", tags=["د اډمین اداره"])

@router.get("/books", response_model=list[BookPublic])
def all_books(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    books = db.scalars(select(Book).order_by(Book.created_at.desc()).limit(300)).all()
    return [to_public(book) for book in books]

@router.post("/books/{book_id}/approve")
def approve_book(book_id: int, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="کتاب ونه موندل شو.")
    book.status = "approved"
    db.commit()
    return {"message": "کتاب تایید شو."}

@router.delete("/books/{book_id}")
def delete_book(book_id: int, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="کتاب ونه موندل شو.")
    db.delete(book)
    db.commit()
    return {"message": "کتاب حذف شو."}

@router.get("/users", response_model=list[UserPublic])
def list_users(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.scalars(select(User).order_by(User.created_at.desc()).limit(500)).all()
    return users
