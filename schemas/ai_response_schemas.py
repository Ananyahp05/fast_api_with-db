from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AIRequest(BaseModel):
    message: str
    user_email: str
    session_id: Optional[int] = None
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str
    session_id: int

class MessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionSchema(BaseModel):
    id: int
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    history: List[SessionSchema]

class SessionDetailResponse(BaseModel):
    id: int
    messages: List[MessageSchema]
