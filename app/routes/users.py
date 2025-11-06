from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import logging

logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()
security = HTTPBearer()
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# User model
class User(BaseModel):
    id: int
    name: str
    email: str

# In-memory DB
users_db = []

# users
users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "deepak": {"username": "deepak", "password": "deepak123", "role": "user"},
    "kulkarni": {"username": "kulkarni", "password": "kulkarni123", "role": "user"}
}

# JWT helpers
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    print("Creating token with payload:", jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("JWT verification running")
    token = credentials.credentials
    print("Token received:", token[:30])  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        print("Token expired")
        raise HTTPException(status_code=401, Error="Token expired")
    except jwt.InvalidTokenError as e:
        print("Invalid token:", e)
        raise HTTPException(status_code=401, Error="Invalid token")

    print("Payload decoded successfully:", payload)
    return payload

def authorize(user, path, method):
    if user["role"] != "admin" and method == "POST":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    return True

# Login route
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    user = users.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    logging.info("Login for user: ".format(username=data.username))
    return {"access_token": token, "token_type": "bearer"}

# Get all users (requires authentication)
@router.get("/users", response_model=List[User])
def get_users(current_user: dict = Depends(verify_jwt)):
    authorize(current_user, "/users", "GET")
    return users_db

# Create user (admin only)
@router.post("/users", response_model=User)
def create_user(user: User, current_user: dict = Depends(verify_jwt)):
    authorize(current_user, "/users", "POST")
    users_db.append(user)
    return user
