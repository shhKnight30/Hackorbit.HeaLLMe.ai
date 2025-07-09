# routers/chat.py

from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Dict
from services.ai_service import HealthAIService
from auth import verify_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/chat", tags=["Chat"])

ai_service = HealthAIService()


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    return verify_token(token)

@router.post("/ask")
async def chat_with_ai(
    message: str = Body(..., embed=True),
    chat_history: List[Dict] = Body([], embed=True),
    token: str = Depends(oauth2_scheme)
):
    """
    Chat with HeaLLMe.ai's AI Assistant.

    Request body should include:
    - message: current user message
    - chat_history: list of previous messages (optional)
    """
    user_id = verify_token(token)
    user_data = {"user_id": user_id}  # Can be expanded with more profile info later

    try:
        response = await ai_service.chat_with_ai(message, chat_history, user_data)
        return {
            "user_message": message,
            "ai_response": response
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat failed: {str(e)}"
        )
