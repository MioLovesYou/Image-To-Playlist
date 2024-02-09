from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No image part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected image', 400
    if file:
        # Save the file to a directory (adjust 'uploads/' to your preferred path)
        filename = file.filename
        save_path = os.path.join('uploads', filename)
        file.save(save_path)
        return 'Image successfully uploaded', 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the server on port 8000
