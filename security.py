import hashlib
import hmac
import secrets
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User

def _serializer():
    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY چاپېریالي متغیر نه دی ټاکل شوی.")
    return URLSafeTimedSerializer(settings.SECRET_KEY, salt="afghan-library-access")

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    return f"{salt.hex()}${digest.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, digest_hex = stored_hash.split("$", 1)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 310_000
        ).hex()
        return hmac.compare_digest(actual, digest_hex)
    except (ValueError, TypeError):
        return False

def create_access_token(user: User) -> str:
    return _serializer().dumps({"user_id": user.id})

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="لومړی خپل حساب ته ننوځئ.")
    try:
        payload = _serializer().loads(
            credentials.credentials,
            max_age=settings.TOKEN_MAX_AGE_SECONDS,
        )
        user_id = int(payload["user_id"])
    except (BadSignature, SignatureExpired, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="د ننوتلو نښه ناسمه یا ختمه شوې ده.")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="دا کارن نور شتون نه لري.")
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="دا کار یوازې اډمین ترسره کولای شي.")
    return user
