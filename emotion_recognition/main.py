import os
from keras import Sequential
from keras.src.layers import Conv2D, Flatten, Dense, MaxPooling2D
from data.dataset_loader import download_dataset, load_data, prepare_generators


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
