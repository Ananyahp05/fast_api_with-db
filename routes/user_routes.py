from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
def signup():
    return {"message": "User created successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}    
    