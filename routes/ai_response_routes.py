from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from db import get_db
from models import User, ChatSession, ChatMessage
from utils.ai_response import get_completion
from schemas.ai_response_schemas import (
    AIRequest, 
    AIResponse, 
    ChatHistoryResponse, 
    SessionDetailResponse,
    SessionSchema,
    MessageSchema
)

router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db)):
    """Get response from AI model and save history."""
    try:
        # 1. Find User
        user = db.query(User).filter(User.email == request.user_email).first()
        if not user:
            # Check if we should create a user implicitly or error out. 
            # For now, let's error if user doesn't specificially sign up, 
            # but since Dashboard.jsx defaults to 4mh23cs010@gmail.com if nothing else, we might need to handle it.
            raise HTTPException(status_code=404, detail="User not found. Please sign up/login first.")

        # 2. Manage Session
        if request.session_id:
            session = db.query(ChatSession).filter(ChatSession.id == request.session_id, ChatSession.user_id == user.id).first()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
        else:
            # Create new session
            # Generate a title based on the first few words of the message
            title = " ".join(request.message.split()[:5]) + "..."
            session = ChatSession(user_id=user.id, title=title)
            db.add(session)
            db.commit()
            db.refresh(session)

        # 3. Save User Message
        user_msg = ChatMessage(
            session_id=session.id,
            role='user',
            content=request.message
        )
        db.add(user_msg)
        
        # 4. Get AI Response
        ai_text = get_completion(request.message, request.system_prompt)
        
        # 5. Save AI Response
        ai_msg = ChatMessage(
            session_id=session.id,
            role='assistant',
            content=ai_text
        )
        db.add(ai_msg)
        
        db.commit()

        return AIResponse(response=ai_text, session_id=session.id)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat_history", response_model=ChatHistoryResponse)
def get_chat_history(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return ChatHistoryResponse(history=[])
    
    sessions = db.query(ChatSession).filter(ChatSession.user_id == user.id).order_by(desc(ChatSession.created_at)).all()
    
    return ChatHistoryResponse(history=[SessionSchema.from_orm(s) for s in sessions])

@router.get("/chat_history/{session_id}", response_model=SessionDetailResponse)
def get_session_detail(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # We need to manually construct the messages list to match MessageSchema if needed,
    # or rely on from_orm if everything aligns perfectly. 
    # Logic in frontend expects { messages: [...] }
    
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    
    return SessionDetailResponse(
        id=session.id,
        messages=[MessageSchema.from_orm(m) for m in messages]
    ) 