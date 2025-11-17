from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..services import AuthService
from ..models import User
from ..schemas import UserCreate, Token, UserResponse
from ..utils.logger import get_logger

router = APIRouter()
auth_service = AuthService()
logger = get_logger(__name__)

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = auth_service.get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": db_user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    email: str = Form(..., alias="username"),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token"""
    logger.info(f"Login attempt for email: {email}")

    user = auth_service.authenticate_user(db, email, password)
    if not user:
        logger.warning(f"Failed login attempt for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Successful login for user: {user.email} (ID: {user.id})")
    access_token = auth_service.create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(auth_service.get_current_user_dependency)):
    """Get current user information"""
    logger.info(f"User info requested for: {current_user.email}")
    return UserResponse.model_validate(current_user)