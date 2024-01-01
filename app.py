from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)


model_path = 'model/model.h5'  # Update with your model path
model = load_model(model_path)


with open('remedies.json', 'r') as file:
    remedies_data = json.load(file)


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
        os.makedirs(uploads_folder, exist_ok=True) 

        file_path = os.path.join(uploads_folder, secure_filename(file.filename))
        file.save(file_path)


        img = image.load_img(file_path, target_size=(image_height, image_width))
        os.remove(file_path) 

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0


        prediction = model.predict(img_array)


        class_indices = { 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Proliferative DR'} 
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_indices[predicted_class_index]


        remedy = remedies_data.get(predicted_class, "No remedy available")

        print(f"Predicted Class: {predicted_class}")
        print(f"Remedy: {remedy}")  

        return jsonify({'result': predicted_class, 'remedy': remedy})

if __name__ == '__main__':
    app.run(debug=True)
