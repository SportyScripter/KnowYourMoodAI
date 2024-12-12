import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Union
from fastapi import FastAPI

app = FastAPI()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@app.get("/")
def read_root():
    return {"Hello, ": "What is your mood?"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}