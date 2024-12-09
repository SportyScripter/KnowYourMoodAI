import os
from keras import Sequential
from keras.src.layers import Conv2D, Flatten, Dense, MaxPooling2D

from WebApp.main import app
from data.dataset_loader import download_dataset, load_data, prepare_generators
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from model.inference import predict_emotion  # Funkcja do predykcji
import os

MODEL_PATH = os.path.join("saved_model", "emotion_model.h5")


@app.post("/analyze-emotion/")
async def analyze_emotion(file: UploadFile = File(...)):
    """
    Endpoint przyjmujący obraz, który analizuje emocje.
    Args:
        file (UploadFile): Przesłany obraz.

    Returns:
        JSONResponse: Przewidywana emocja.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Nieprawidłowy format obrazu.")

        # Przygotowanie obrazu (rozmiar i normalizacja)
        image = cv2.resize(image, (48, 48))  # Rozmiar zgodny z modelem
        image = image.astype('float32') / 255.0
        image = np.expand_dims(image, axis=(0, -1))  # Dodanie wymiarów batch i kanału

        # Predykcja emocji
        emotion = predict_emotion(image, MODEL_PATH)

        return JSONResponse(content={"emotion": emotion})

   # except Exception as e:
  #      raise HTTPException(status_code=400, detail=f"Błąd przetwarzania: {str(e)}")
def main():
    dataset_path = download_dataset()
    data_path = os.path.join(dataset_path, "data")

    train_images, test_images, train_labels, test_labels = load_data(data_path)

    train_generator, test_generator = prepare_generators(train_images, train_labels, test_images, test_labels)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(set(train_labels)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_generator, epochs=10, validation_data=test_generator)

if __name__ == "__main__":
    main()
