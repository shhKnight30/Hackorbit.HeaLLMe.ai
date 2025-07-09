from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatMessageBase(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    message_type: str = Field("health_guidance", regex="^(health_guidance|symptom_check|health_advice)$")

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: str
    user_id: str
    response: str
    timestamp: datetime
    session_id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "message": "I have been feeling tired lately",
                "response": "I understand you're feeling tired. Can you tell me more about your symptoms?",
                "timestamp": "2024-01-01T10:00:00Z",
                "session_id": "507f1f77bcf86cd799439013",
                "message_type": "health_guidance"
            }
        }

class ChatSessionBase(BaseModel):
    session_name: str = Field(..., max_length=200)

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionUpdate(BaseModel):
    session_name: Optional[str] = Field(None, max_length=200)

class ChatSessionResponse(ChatSessionBase):
    id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "session_name": "Health Consultation",
                "created_at": "2024-01-01T10:00:00Z",
                "last_activity": "2024-01-01T10:01:00Z",
                "messages": [
                    {
                        "id": "507f1f77bcf86cd799439013",
                        "user_id": "507f1f77bcf86cd799439012",
                        "message": "I have been feeling tired lately",
                        "response": "I understand you're feeling tired. Can you tell me more about your symptoms?",
                        "timestamp": "2024-01-01T10:00:00Z",
                        "session_id": "507f1f77bcf86cd799439011",
                        "message_type": "health_guidance"
                    }
                ]
            }
        }

class ChatSessionListResponse(BaseModel):
    id: str
    session_name: str
    last_message: Optional[str] = None
    message_count: int
    last_activity: datetime
    created_at: datetime

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    message_type: str = Field("health_guidance", regex="^(health_guidance|symptom_check|health_advice)$")

class ChatMessageResponse(BaseModel):
    message: ChatMessageResponse
    ai_response: ChatMessageResponse
    health_insights: Optional[Dict[str, Any]] = {}
    recommendations: Optional[List[str]] = []

class ChatSummary(BaseModel):
    session_id: str
    session_name: str
    summary: str
    key_symptoms: List[str] = []
    recommendations: List[str] = []
    created_at: datetime
