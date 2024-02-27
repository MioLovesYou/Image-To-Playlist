from flask import Flask, request
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained model (provide the correct path to your model file)
model = load_model('models/model.h5')

# Load WNIDs and labels
wnids = []
wnid_to_label = {}
with open('../../datasets/tiny-imagenet-200/wnids.txt', 'r') as f:
    wnids = [line.strip() for line in f.readlines()]

with open('../../datasets/tiny-imagenet-200/words.txt', 'r') as f:
    for line in f:
        wnid, label = line.strip().split('\t', 1)
        wnid_to_label[wnid] = label

# Function to convert model output to labels
def get_labels_from_output(output_array):
    # Find the index of the highest probability
    top_indices = output_array.argsort()[-5:][::-1]  # Get top 5 indices, for example
    # Get the corresponding wnids and labels
    labels = [wnid_to_label[wnids[idx]] for idx in top_indices]
    return labels

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No image part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected image', 400
    if file:
        # Save the file to a directory
        filename = file.filename
        save_path = os.path.join('uploads', filename)
        file.save(save_path)

        # Preprocess the image
        img = image.load_img(save_path, target_size=(64, 64))  # Adjust target_size as per your model's input layer
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create a batch
        img_array /= 255.0  # Normalize to [0,1]

        # Predict the sentiment or tags
        predictions = model.predict(img_array)

        # Convert predictions to labels
        labels = get_labels_from_output(predictions.flatten())

        # Output human-readable labels to console
        print(labels)

        return 'Image successfully uploaded and processed', 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
