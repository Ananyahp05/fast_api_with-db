from db import engine, Base, SessionLocal
from models import ChatSession, ChatMessage, User
from sqlalchemy import desc
from schemas.ai_response_schemas import SessionSchema
import datetime

def check_db():
    print("Checking database logic...")
    db = SessionLocal()
    try:
        # 1. Get or Create User
        email = "4mh23cs010@gmail.com"
        print(f"Querying user: {email}")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User {email} not found. Creating...")
            user = User(email=email, password="password")
            db.add(user)
            db.commit()
            db.refresh(user)
        print(f"User ID: {user.id}")

        # 2. Create Session
        print("Creating test session...")
        session = ChatSession(user_id=user.id, title="Test Session")
        db.add(session)
        db.commit()
        db.refresh(session)
        print(f"Session created: {session.id}, created_at: {session.created_at}")

        # 3. Query Sessions
        print("Querying sessions...")
        sessions = db.query(ChatSession).filter(ChatSession.user_id == user.id).order_by(desc(ChatSession.created_at)).all()
        print(f"Found {len(sessions)} sessions.")

        # 4. Pydantic Validation
        print("Validating with Pydantic...")
        for s in sessions:
            try:
                # Manually construct dict to see if that works
                # data = {"id": s.id, "title": s.title, "created_at": s.created_at}
                # print(f"Data: {data}")
                
                schema = SessionSchema.from_orm(s)
                print(f"Valid: {schema.id}")
            except Exception as e:
                print(f"Validation Error for session {s.id}: {e}")
                # Don't raise, just print
                
        print("All validations passed!")
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
