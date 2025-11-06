from fastapi import HTTPException
from app.models import User

# In-memory "database"
users_db = []

def get_all_users():
    return users_db

def add_user(user: User):
    # Check for duplicate user ID
    if any(u["id"] == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="User with this ID already exists.")
    users_db.append(user.dict())
    return user
