# Diabetic Retinopathy Detection..


## Introduction

This project is focused on employing machine learning techniques to detect diabetic retinopathy using fundus images of the retina. Diabetic retinopathy is a severe complication of diabetes affecting the eyes, potentially leading to blindness if not addressed.

## Technologies Used

The technologies utilized in this project include:

- **Python**: Backend programming language.
- **Flask**: Web framework for the application.
- **TensorFlow/Keras**: Deep learning library used for model development and predictions.
- **JSON**: Data format for storing remedies associated with different stages of retinopathy.
- **HTML/CSS/JS**: Frontend development for user interaction.

## Overview

The project consists of a Flask-based web application that serves as an interface for diabetic retinopathy detection. It involves the following functionalities:

1. **Model Loading**: Load a pre-trained machine learning model capable of detecting retinopathy from fundus images.

2. **Image Processing**: Process uploaded fundus images for prediction.

3. **Prediction and Remedies**: Provide predictions on the severity of diabetic retinopathy and suggest remedies based on the prediction outcome.

## Instructions to Run

### Prerequisites

Ensure the following requirements are met:

- **Python**: Ensure Python 3.x is installed on your system.

### Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/your-project.git
    cd diabetic_retinopathy
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare Model and Files:**

    - Place your trained model file (`model.h5`) in a folder named `model` within your project directory.
    - Ensure the `remedies.json` file contains remedies associated with different stages of retinopathy.

### Running the Application

4. **Run the Flask Application:**

    ```bash
    python app.py
    ```

    

5. **Access the Application:**

    - Open a web browser and visit [http://localhost:5000](http://localhost:5000) (or the address specified in your Flask code if modified) to access the Diabetic Retinopathy Detection application.
    - Use the provided interface to upload fundus images and view the predictions and suggested remedies.

6. **Troubleshooting:**

    - If any issues occur, ensure proper file paths in your Flask code for loading the model (`'model/model.h5'`) and the remedies JSON file (`'remedies.json'`).
    - Check the console or terminal for error messages that might help identify problems.
