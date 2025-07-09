from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta
from auth import get_password_hash, verify_password, create_access_token
from schema.user import UserCreate, UserLogin, UserResponse, UserUpdate
from schema.health_data import HealthDataResponse
from uuid import uuid4
from datetime import datetime
import database  # Assume this is your user DB interaction layer
from services.notifications import notify_user_registration
from fastapi import Request

router = APIRouter(prefix="/users", tags=["Users"])

# Mock in-memory user database
users_db = {}

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid4())
    hashed_password = get_password_hash(user.password)
    
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "height": user.height,
        "medical_history": user.medical_history,
        "allergies": user.allergies,
        "medications": user.medications,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    await notify_user_registration(user_id, user.email, user.username)

    return UserResponse(
        id=user_id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        age=user.age,
        gender=user.gender,
        weight=user.weight,
        height=user.height,
        medical_history=user.medical_history,
        allergies=user.allergies,
        medications=user.medications,
        is_active=True,
        is_verified=False,
        created_at=users_db[user.email]["created_at"],
        updated_at=users_db[user.email]["updated_at"]
    )

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends()):
    # A real application would use a dependency to extract user from token
    username = token  # Placeholder
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        full_name=user["full_name"],
        age=user["age"],
        gender=user["gender"],
        weight=user["weight"],
        height=user["height"],
        medical_history=user["medical_history"],
        allergies=user["allergies"],
        medications=user["medications"],
        is_active=user["is_active"],
        is_verified=user["is_verified"],
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )

@router.put("/me", response_model=UserResponse)
def update_user_profile(update_data: UserUpdate, token: str = Depends()):
    username = token  # Placeholder for token-based user extraction
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        user[field] = value
    user["updated_at"] = datetime.utcnow()

    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        full_name=user.get("full_name"),
        age=user.get("age"),
        gender=user.get("gender"),
        weight=user.get("weight"),
        height=user.get("height"),
        medical_history=user.get("medical_history", []),
        allergies=user.get("allergies", []),
        medications=user.get("medications", []),
        is_active=user["is_active"],
        is_verified=user["is_verified"],
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )
