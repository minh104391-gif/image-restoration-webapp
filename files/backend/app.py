from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from image_filters import (
    apply_bilateral_filter,
    apply_nlm_filter,
    apply_wiener_filter,
    apply_notch_filter
)
from noise_handling import add_gaussian_noise, add_salt_pepper_noise, add_periodic_noise
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload an image file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filter', methods=['POST'])
def apply_filter():
    """Apply selected filter to image"""
    try:
        data = request.json
        filepath = data.get('filepath')
        filter_type = data.get('filter')
        noise_type = data.get('noise_type')
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Read image
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Apply filter based on selection
        if filter_type == 'bilateral':
            result = apply_bilateral_filter(image)
        elif filter_type == 'nlm':
            result = apply_nlm_filter(image)
        elif filter_type == 'wiener':
            result = apply_wiener_filter(image)
        elif filter_type == 'notch':
            result = apply_notch_filter(image)
        else:
            return jsonify({'error': 'Unknown filter type'}), 400
        
        # Encode result
        _, buffer = cv2.imencode('.png', result)
        img_io = BytesIO(buffer)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png'), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-noise', methods=['POST'])
def add_noise():
    """Add noise to image"""
    try:
        data = request.json
        filepath = data.get('filepath')
        noise_type = data.get('noise_type')
        intensity = float(data.get('intensity', 0.1))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Read image
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Convert to float
        image = image.astype(np.float32) / 255.0
        
        # Add noise
        if noise_type == 'gaussian':
            noisy_image = add_gaussian_noise(image, intensity)
        elif noise_type == 'salt_pepper':
            noisy_image = add_salt_pepper_noise(image, intensity)
        elif noise_type == 'periodic':
            noisy_image = add_periodic_noise(image, intensity)
        else:
            return jsonify({'error': 'Unknown noise type'}), 400
        
        # Convert back to uint8
        noisy_image = np.clip(noisy_image * 255, 0, 255).astype(np.uint8)
        
        # Save noisy image
        noisy_filepath = filepath.replace('.', '_noisy.')
        cv2.imwrite(noisy_filepath, noisy_image)
        
        # Encode result
        _, buffer = cv2.imencode('.png', noisy_image)
        img_io = BytesIO(buffer)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png'), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)