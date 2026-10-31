"""Authentication and User Session API Routes."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user_required
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account with hashed password and return JWT."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name or user_in.email.split("@")[0]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "email": new_user.email})
    return TokenResponse(
        access_token=token,
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        is_guest=False
    )


@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticate existing credentials and issue JWT."""
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token({"sub": user.id, "email": user.email})
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_guest=False
    )


@router.post("/guest", response_model=TokenResponse)
def guest_login():
    """Create an instant guest session allowing full platform trial without prior signup."""
    guest_id = f"guest-{uuid.uuid4().hex[:8]}"
    token = create_access_token({"sub": guest_id, "email": f"{guest_id}@skillsync.io"})
    return TokenResponse(
        access_token=token,
        user_id=guest_id,
        email=f"{guest_id}@skillsync.io",
        full_name="Guest Professional",
        is_guest=True
    )


@router.get("/me", response_model=UserOut)
def get_current_user_profile(user: dict = Depends(get_current_user_required), db: Session = Depends(get_db)):
    """Retrieve details of the currently authenticated account."""
    db_user = db.query(User).filter(User.id == user["sub"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User account not found.")
    return UserOut(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        created_at=db_user.created_at.isoformat() if db_user.created_at else None
    )
