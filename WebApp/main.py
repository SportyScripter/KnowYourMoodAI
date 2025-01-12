from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import bcrypt
import os
import sys

from fastapi.middleware.cors import CORSMiddleware


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pydantic import EmailStr
import numpy as np
import cv2
from deepface import DeepFace


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


DATABASE_URL = "sqlite:///./user-data.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Database Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# Create database tables
Base.metadata.create_all(bind=engine)


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility functions
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_user_by_username_or_email(db: Session, username_or_email: str):
    return db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()


def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Endpoints
@app.get("/")
def read_root():
    return {"message": "Hello, what is your mood?"}

@app.post("/analyze-emotion/")
async def analyze_emotion(file: UploadFile = File(...)):
    try:
        # Read file contents into memory
        contents = await file.read()

        # Convert to numpy array for DeepFace
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        try:
            analysis = DeepFace.analyze(
                img_path=img,  # Pass image array directly instead of file path
                actions=['emotion'],
                enforce_detection=True,
                detector_backend='opencv'  # Explicitly specify detector for better performance
            )
            # Standardize output format
            if isinstance(analysis, dict):
                analysis = [analysis]

        except Exception as e:
            print("Error during face detection or emotion analysis:", e)
            raise HTTPException(
                status_code=400,
                detail="Failed to detect face or analyze emotion",
            ) from e

        emotion = analysis[0]['dominant_emotion']
        return JSONResponse(content={
            "emotion": emotion,
        })

    except Exception as e:
        print("error", e)
        raise HTTPException(
            status_code=400, 
            detail=f"Error processing image: {str(e)}"
        ) from e


@app.post("/register/")
def register(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user_by_username = db.query(User).filter(User.username == username).first()
    user_by_email = db.query(User).filter(User.email == email).first()
    if user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, username, email, password)
    return {"message": "User registered successfully"}


@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username_or_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

