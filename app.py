from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename
import json
import pyrebase
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
#
firebase_config = {
    "apiKey": "AIzaSyAeUlVTBZiAPXRJ2Tsg-BqkmDqbzAOBylA",
    "authDomain": "diabeticretinopathy-auth.firebaseapp.com",
    "projectId": "diabeticretinopathy-auth",
    "storageBucket": "diabeticretinopathy-auth.appspot.com",
    "messagingSenderId": "442020803694",
    "appId": "your_app_id",
    "measurementId": "1:442020803694:web:cdc11e82ffba7c42aea27f",
    "databaseURL":""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Load model
model_path = 'model/model.h5'
model = load_model(model_path)

with open('remedies.json', 'r') as file:
    remedies_data = json.load(file)

image_height = 150
image_width = 150

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect(url_for('home'))
        except Exception as e:
            error_message = str(e)
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except Exception as e:
            error_message = str(e)
            return render_template('signup.html', error=error_message)
    return render_template('signup.html')


@app.route('/predict')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/predict-disease', methods=['POST'])
def predict():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized access'}), 403

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

        class_indices = {0: 'Mild', 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Proliferative DR'}
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_indices[predicted_class_index]

        remedy = remedies_data.get(predicted_class, "No remedy available")

        return jsonify({'result': predicted_class, 'remedy': remedy})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
