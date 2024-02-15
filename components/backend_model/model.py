import tensorflow as tf
from tensorflow.keras import layers, models
num_classes = 200 #sentiments we're collecting

def build_model(input_shape):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    # Add more layers as needed
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))  # num_classes is the number of sentiments
    return model
