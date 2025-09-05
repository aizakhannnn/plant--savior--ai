from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
import os
from PIL import Image
import uuid

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model and treatments
def load_model_and_treatments():
    try:
        model = tf.keras.models.load_model('best_plant_model_final.keras')
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        return model, treatments
    except Exception as e:
        print(f"Error loading model or treatments: {e}")
        return None, {}

# Load model and treatments on startup
model, treatments = load_model_and_treatments()
class_names = list(treatments.keys()) if treatments else []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    if file:
        # Generate unique filename
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Preprocess image
            img = load_img(filepath, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = img_array.reshape(1, 224, 224, 3) / 255.0
            
            # Make prediction
            predictions = model.predict(img_array, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence_score = float(predictions[0][predicted_class])
            
            # Get prediction details
            predicted_disease = class_names[predicted_class] if predicted_class < len(class_names) else "Unknown"
            treatment = treatments.get(predicted_disease, "Consult agricultural expert.")
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'prediction': predicted_disease,
                'confidence': confidence_score,
                'treatment': treatment
            })
        except Exception as e:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(debug=True)