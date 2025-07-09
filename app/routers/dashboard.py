from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from schema.health_data import HealthInsightsResponse
from schema.user import UserResponse
from services.ai_service import HealthAIService
from auth import verify_token
from fastapi.security import OAuth2PasswordBearer
from db.fake_user_db import get_user_by_username  # Replace with real DB logic  just for testing only

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
ai_service = HealthAIService()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    username = verify_token(token)
    user = await get_user_by_username(username)  # Replace with your DB call later/...
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/quote", summary="Get a daily health quote")
async def get_daily_quote():
    return {"quote": ai_service.get_daily_health_quote()}


@router.post("/analyze-symptoms", summary="Analyze user symptoms with AI")
async def analyze_symptoms(payload: Dict[str, Any], user: UserResponse = Depends(get_current_user)):
    symptoms = payload.get("symptoms", "")
    if not symptoms:
        raise HTTPException(status_code=400, detail="Symptoms are required")
    result = await ai_service.analyze_symptoms(
        symptoms=symptoms,
        user_history=user.medical_history or [],
        user_data=user.model_dump()
    )
    return result


@router.post("/recommendations", summary="Get AI-generated health recommendations")
async def get_recommendations(user: UserResponse = Depends(get_current_user)):
    user_data = user.model_dump()
   
    user_data["health_data"] = {}  
    user_data["lifestyle"] = {}    
    return await ai_service.generate_health_recommendations(user_data)


@router.post("/analyze-health", summary="Analyze health data for insights", response_model=HealthInsightsResponse)
async def analyze_health_data(payload: Dict[str, Any], user: UserResponse = Depends(get_current_user)):
    result = await ai_service.analyze_health_data(payload, user.model_dump())
    return result
