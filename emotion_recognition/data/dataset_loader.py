import os
import kagglehub
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd

def download_dataset():
    path = kagglehub.dataset_download("sanidhyak/human-face-emotions")
    print("Path to dataset files:", path)
    return path

def load_data(dataset_path, test_size=0.2):
    data = pd.read_csv(os.path.join(dataset_path, "data.csv"))  # Załóżmy, że zbiór jest w formacie CSV
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)
    return train_data, test_data

def prepare_generators(train_data, test_data, img_size=(48, 48), batch_size=32):
    train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_dataframe(
        train_data,
        x_col="image_path",
        y_col="emotion",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical"
    )
    test_generator = test_datagen.flow_from_dataframe(
        test_data,
        x_col="image_path",
        y_col="emotion",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical"
    )
    return train_generator, test_generator
