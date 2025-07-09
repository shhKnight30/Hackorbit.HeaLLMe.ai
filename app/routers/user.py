from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.auth import verify_password, get_password_hash, create_access_token, verify_token
from app.database.connection import get_database
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from datetime import timedelta, datetime
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    db = await get_database()
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_data = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        age=user.age,
        gender=user.gender
    )
    result = await db.users.insert_one(user_data.dict(by_alias=True))
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = await get_database()
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    # Update last login
    await db.users.update_one(
        {"username": form_data.username},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    return {"access_token": access_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES, "user_id": str(user["_id"])}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    db = await get_database()
    user = await db.users.find_one({"username": username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
