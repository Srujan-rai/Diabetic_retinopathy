from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

# Load your pre-trained model
model_path = 'model/model.h5'  # Update with your model path
model = load_model(model_path)

# Load remedies from JSON file
with open('remedies.json', 'r') as file:
    remedies_data = json.load(file)

# Define image properties
image_height = 150
image_width = 150

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No image file selected'})


    if file:
        uploads_folder = 'uploads'
        os.makedirs(uploads_folder, exist_ok=True)  # Create the 'uploads' folder if it doesn't exist

        file_path = os.path.join(uploads_folder, secure_filename(file.filename))
        file.save(file_path)

        # Load and preprocess the image
        img = image.load_img(file_path, target_size=(image_height, image_width))
        os.remove(file_path)  # Remove the uploaded file after loading

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Rescale pixel values

        # Make prediction
        prediction = model.predict(img_array)

        # Mapping class indices to class labels
        class_indices = { 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Proliferative DR'}  # Update with your class indices
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_indices[predicted_class_index]


        remedy = remedies_data.get(predicted_class, "No remedy available")

        print(f"Predicted Class: {predicted_class}")
        print(f"Remedy: {remedy}")  # Ensure remedies_data is loaded correctly

        return jsonify({'result': predicted_class, 'remedy': remedy})

if __name__ == '__main__':
    app.run(debug=True)
