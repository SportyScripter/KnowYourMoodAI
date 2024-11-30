import numpy as np

def predict_emotion(model, image, class_labels):
    predictions = model.predict(np.expand_dims(image, axis=0))
    predicted_class = np.argmax(predictions, axis=1)[0]
    return class_labels[predicted_class]
