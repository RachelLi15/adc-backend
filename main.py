from fastapi import FastAPI, Depends
from pydantic import BaseModel
import jwt
import datetime
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from contextlib import asynccontextmanager
from routers import lecture, slack, homework, attendance, mentors

origins = [
     "http://localhost:5173",
     "http://localhost",
    "http://localhost:5174",    
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",    
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# including the routers to different files
app.include_router(lecture.router, tags=["Lectures"])
app.include_router(slack.router, tags=["Slack"])
app.include_router(homework.router, tags=["Homeworks"])
app.include_router(attendance.router, tags=["Attendance"])
app.include_router(mentors.router, tags=["Mentors"])

# # Add CORS middleware to allow access from any origin
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )


# Secret key for encoding and decoding JWT token (Keep this secret in production)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"  # The algorithm for encoding the JWT

# Pydantic model for the request body
class UserRequest(BaseModel):
    email: str

# Function to generate JWT token
def create_jwt_token(email: str) -> str:
    # JWT expiration time (e.g., 15 minutes)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    # Payload containing the user's email
    payload = {"email": email, "exp": expiration_time}
    
    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Endpoint to generate the JWT token
@app.post("/generate-jwt/")
async def generate_jwt(user: UserRequest) -> Dict[str, str]:
    # Extract email from the request
    email = user.email
    
    # Create JWT token using the provided email
    token = create_jwt_token(email)
    
    # Return the token in the response
    return {"access_token": token, "token_type": "bearer"}

# Run the server with: uvicorn filename:app --reload


