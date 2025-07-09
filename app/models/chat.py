from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime,timezone
from bson import ObjectId

class ChatMessage(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    session_id: str
    message_type: str = "health_guidance"  # symptom_check, health_advice, etc.
    
class ChatSession(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    session_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    messages: List[ChatMessage] = []
