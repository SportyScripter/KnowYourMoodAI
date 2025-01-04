from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Form
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pydantic import BaseModel, EmailStr
from typing import Union
import numpy as np
import cv2
from emotion_recognition.model.inference import predict_emotion


app = FastAPI()

MODEL_PATH = os.path.join("saved_model", "emotion_model.h5")
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    return {"Hello, ": "What is your mood?"}



@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())
        return JSONResponse(
            content={
                "filename": file.filename,
                "file_path": file_path,
                "type": file.content_type,
                "message": "File successfully uploaded.",
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/analyze-emotion/")
async def analyze_emotion(file: UploadFile = File(...)):
    """
    Endpoint for analyzing emotions from an uploaded image.
    Args:
        file (UploadFile): Uploaded image file.

    Returns:
        JSONResponse: Predicted emotion.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Invalid image format.")

        # Preprocess the image (resize and normalize)
        image = cv2.resize(image, (48, 48))  # Resize to match model input
        image = image.astype('float32') / 255.0
        image = np.expand_dims(image, axis=(0, -1))  # Add batch and channel dimensions

        # Predict emotion
        emotion = predict_emotion(image, MODEL_PATH)

        return JSONResponse(content={"emotion": emotion})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


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

