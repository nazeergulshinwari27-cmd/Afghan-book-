from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Book, User
from app.schemas import BookPublic
from app.security import get_current_user, get_current_admin

router = APIRouter(prefix="/api/books", tags=["کتابونه"])

def to_public(book: Book) -> BookPublic:
    return BookPublic(
        id=book.id, title=book.title, author=book.author,
        category=book.category, description=book.description,
        owner_id=book.owner_id, status=book.status, created_at=book.created_at,
    )

@router.get("/", response_model=list[BookPublic])
def list_books(q: str = "", category: str = "", db: Session = Depends(get_db)):
    query = select(Book).where(Book.status == "approved")
    if q.strip():
        pattern = f"%{q.strip()}%"
        query = query.where(or_(
            Book.title.ilike(pattern),
            Book.author.ilike(pattern),
            Book.description.ilike(pattern),
        ))
    if category.strip() and category.strip() != "ټولې":
        query = query.where(Book.category == category.strip())
    results = db.scalars(query.order_by(Book.created_at.desc()).limit(100)).all()
    return [to_public(book) for book in results]

@router.post("/", response_model=BookPublic, status_code=201)
async def upload_book(
    title: str = Form(..., min_length=1, max_length=180),
    author: str = Form("نامعلوم", max_length=140),
    category: str = Form("نور", max_length=80),
    description: str = Form("", max_length=3000),
    pdf_file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    filename = (pdf_file.filename or "").replace("\\", "/").split("/")[-1]
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="یوازې PDF فایل منل کېږي.")
    content = await pdf_file.read(settings.MAX_UPLOAD_BYTES + 1)
    if len(content) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="د PDF فایل اندازه باید تر ۲۰ MB زیاته نه وي.")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="پورته شوی فایل سم PDF نه دی.")
    book = Book(
        title=title.strip(),
        author=author.strip() or "نامعلوم",
        category=category.strip() or "نور",
        description=description.strip(),
        original_filename=filename[:255],
        pdf_data=content,
        owner_id=user.id,
        status="approved" if user.role == "admin" else "pending",
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return to_public(book)

@router.get("/mine", response_model=list[BookPublic])
def my_books(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    results = db.scalars(
        select(Book).where(Book.owner_id == user.id).order_by(Book.created_at.desc())
    ).all()
    return [to_public(book) for book in results]

@router.get("/{book_id}/pdf")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None or book.status != "approved":
        raise HTTPException(status_code=404, detail="کتاب ونه موندل شو یا لا تایید شوی نه دی.")
    headers = {
        "Content-Disposition": f'inline; filename="book-{book.id}.pdf"',
        "X-Content-Type-Options": "nosniff",
        "Cache-Control": "private, max-age=3600",
    }
    return Response(content=book.pdf_data, media_type="application/pdf", headers=headers)
