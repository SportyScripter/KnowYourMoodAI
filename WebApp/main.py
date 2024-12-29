import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
import numpy as np
import cv2
from model.inference import predict_emotion  # Ensure this import is correctly resolved

app = FastAPI()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MODEL_PATH = os.path.join("saved_model", "emotion_model.h5")

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

@app.get("/")
def read_root():
    return {"Hello, ": "What is your mood?"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
