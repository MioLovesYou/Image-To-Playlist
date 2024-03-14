from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import json

app = Flask(__name__)
CORS(app)

model = load_model('models/model.h5')

# Assuming the labels correspond to the questions in your CSV, in order.
labels = [f"Q{i}" for i in range(1, 130)]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No image part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected image', 400
    if file:
       # ssave the file to upload (/uploads)
        filename = file.filename
        save_path = os.path.join('uploads', filename)
        file.save(save_path)

        # preprocess the image 
        img = image.load_img(save_path, target_size=(224, 224))  # adjust target_size to match model
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # create a batch
        img_array /= 255.0  # normalize into 0-1

        predictions = model.predict(img_array).flatten()

        # Map predictions to labels
        prediction_labels = dict(zip(labels, predictions))

        # Sort by highest chance (probability)
        sorted_predictions = sorted(prediction_labels.items(), key=lambda x: x[1], reverse=True)

        # Convert sorted predictions to a more friendly format
        sorted_predictions_dict = [{"label": label, "probability": float(probability)} for label, probability in sorted_predictions]
        
        print(sorted_predictions_dict)

        # Return sorted predictions
        return jsonify(sorted_predictions_dict), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
