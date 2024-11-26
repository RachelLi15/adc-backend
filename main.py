from fastapi import FastAPI, Depends
from pydantic import BaseModel
import jwt
import datetime
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Field, Session, SQLModel, create_engine

#this is the code for the storing the data and using a database

sqlite_database_name = "data.db"
sqlite_url = f"sqlite:///{sqlite_database_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
# Creating the session, the session communicates with the database
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Lecture(SQLModel, table=True):
    id: int = Field(primary_key=True)
    slideName: str
    url: str

class Homework(SQLModel, table=True):
    id: int = Field(primary_key=True)
    hwName: str
    url: str

class Slack(SQLModel, table=True):
    id: int = Field(primary_key=True)
    slackName: str
    url: str
    slackChannel: str

class Attendance(SQLModel, table=True):
    id: int = Field(primary_key=True)
    studentName: str
    attendance: str
    date: str

class Mentors(SQLModel, table=True):
    id: int = Field(primary_key=True)
    mentorName: str
    mentorEmail: str
    mentorPhone: str
    mentorSlack: str
    
@app.on_event("startup")
def on_startup():
    create_db_and_tables()



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


