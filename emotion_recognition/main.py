from data.dataset_loader import download_dataset, load_data, prepare_generators
from model.training import create_model, train_model
from utils.preprocess import preprocess_image
from model.inference import predict_emotion

def main():
    dataset_path = download_dataset()
    train_data, test_data = load_data(dataset_path)
    train_generator, test_generator = prepare_generators(train_data, test_data)

    class_labels = train_generator.class_indices
    class_labels = {v: k for k, v in class_labels.items()}

    model = create_model()
    train_model(model, train_generator, test_generator)

    # test na jednym obrazie
    test_image_path = test_data.iloc[0]["image_path"]
    image = preprocess_image(test_image_path)
    emotion = predict_emotion(model, image, class_labels)
    print(f"Predicted Emotion: {emotion}")

if __name__ == "__main__":
    main()
