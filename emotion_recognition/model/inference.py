import tensorflow as tf
import numpy as np


def predict_emotion(image, model_path):
    """
    Funkcja przewidująca emocję na podstawie obrazu.

    Args:
        image (np.ndarray): Obraz w formacie NumPy.
        model_path (str): Ścieżka do wytrenowanego modelu.

    Returns:
        str: Przewidywana emocja.
    """
    model = tf.keras.models.load_model(model_path)

    # Przewidywanie
    predictions = model.predict(image)
    emotion_index = np.argmax(predictions)

    # Mapowanie indeksów na etykiety
    emotions = ["Happy", "Sad", "Angry"]
    return emotions[emotion_index]

