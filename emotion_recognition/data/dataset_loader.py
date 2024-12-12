import os
import kagglehub
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


import numpy as np
import cv2


def download_dataset():
    """
    Pobiera zbiór danych za pomocą kagglehub.

    Returns:
        str: Ścieżka do pobranych danych.
    """
    path = kagglehub.dataset_download("sanidhyak/human-face-emotions")
    print("Path to dataset files:", path)
    return path


def load_data(dataset_path, test_size=0.2, img_size=(48, 48)):
    """
    Ładuje dane obrazów z folderów i przypisuje etykiety na podstawie nazw folderów.

    Args:
        dataset_path (str): Ścieżka do folderu z danymi.
        test_size (float): Proporcja danych testowych.
        img_size (tuple): Docelowy rozmiar obrazu.

    Returns:
        tuple: (train_images, train_labels, test_images, test_labels)
    """
    images = []
    labels = []
    classes = os.listdir(dataset_path)  # Pobiera listę folderów (klas)

    for label, class_name in enumerate(classes):
        class_path = os.path.join(dataset_path, class_name)

        if not os.path.isdir(class_path):
            continue  # Pomijamy pliki, które nie są folderami

        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)

            if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Wczytanie w skali szarości
                if image is None:
                    continue  # Pomijamy uszkodzone obrazy

                image = cv2.resize(image, img_size)  # Zmiana rozmiaru
                images.append(image)
                labels.append(label)  # Przypisanie etykiety

    images = np.array(images, dtype='float32') / 255.0  # Normalizacja
    labels = np.array(labels)

    return train_test_split(images, labels, test_size=test_size, random_state=42)


def prepare_generators(train_images, train_labels, test_images, test_labels, batch_size=32):
    """
    Tworzy generatory danych do trenowania i testowania modeli.

    Args:
        train_images (np.ndarray): Obrazy treningowe.
        train_labels (np.ndarray): Etykiety treningowe.
        test_images (np.ndarray): Obrazy testowe.
        test_labels (np.ndarray): Etykiety testowe.
        batch_size (int): Rozmiar batcha.

    Returns:
        tuple: (train_generator, test_generator)
    """
    train_datagen = ImageDataGenerator(rotation_range=30, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator()

    # Przekształcenie obrazów i etykiet do tablic 4D wymaganych przez Keras
    train_images = train_images[..., np.newaxis]
    test_images = test_images[..., np.newaxis]

    train_generator = train_datagen.flow(
        train_images,
        train_labels,
        batch_size=batch_size
    )
    test_generator = test_datagen.flow(
        test_images,
        test_labels,
        batch_size=batch_size
    )

    return train_generator, test_generator
