from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from ..models import User
from ..config import settings
from ..database import get_db

class AuthService:
    def __init__(self):
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            # Ensure both strings are properly encoded
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError as e:
            # Handle bcrypt version compatibility issues
            # Try with different encoding or fallback methods
            try:
                # Some older bcrypt implementations might need different handling
                return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
            except:
                return False
        except Exception:
            return False

    def get_password_hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None

    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        email = self.verify_token(token)
        if email is None:
            return None
        user = db.query(User).filter(User.email == email).first()
        return user

    # FastAPI dependency function
    async def get_current_user_dependency(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        db: Session = Depends(get_db)
    ) -> User:
        """FastAPI dependency to get current authenticated user"""
        token = credentials.credentials
        user = self.get_current_user(db, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def check_permissions(self, user: User, required_role: str) -> bool:
        """Check if user has required role or higher permissions"""
        role_hierarchy = {
            "admin": 4,
            "analyst": 3,
            "counselor": 2,
            "sales": 1
        }

        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level