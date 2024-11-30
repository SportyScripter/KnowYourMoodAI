import cv2
import numpy as np

def preprocess_image(image_path, img_size=(48, 48)):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, img_size)
    image = image / 255.0  # Normalizacja
    return np.expand_dims(image, axis=-1)  # Kanał do wejścia modelu
