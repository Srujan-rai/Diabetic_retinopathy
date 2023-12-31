from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load your pre-trained model
model_path = 'model/model.h5'  # Update with your model path
model = load_model(model_path)

# Define image properties
image_height = 150
image_width = 150

@app.route('/')
def home():
    return render_template('upload.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('upload.html', prediction="No file uploaded")

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html', prediction="No file selected")

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
        class_indices = {0: 'No DR', 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Proliferative DR'}  # Update with your class indices
        predicted_class = class_indices[np.argmax(prediction)]

        return jsonify({'result': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
