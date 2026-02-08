import os
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/output'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure output directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_image_from_url(url):
    """Download image from URL and return as numpy array"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise Exception(f"Error downloading image: {str(e)}")

def add_text_watermark(image, text, position, opacity, scale):
    """Add text watermark to image"""
    overlay = image.copy()
    h, w = image.shape[:2]
    
    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = scale
    thickness = max(1, int(scale * 2))
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Calculate position
    if position == 'top-left':
        x, y = 10, text_height + 10
    elif position == 'top-right':
        x, y = w - text_width - 10, text_height + 10
    elif position == 'bottom-left':
        x, y = 10, h - 10
    elif position == 'bottom-right':
        x, y = w - text_width - 10, h - 10
    else:  # center
        x, y = (w - text_width) // 2, (h + text_height) // 2
    
    # Add text with white background for visibility
    cv2.putText(overlay, text, (x, y), font, font_scale, (255, 255, 255), thickness + 2)
    cv2.putText(overlay, text, (x, y), font, font_scale, (0, 0, 0), thickness)
    
    # Blend with original image
    return cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0)

def add_logo_watermark(image, logo, position, opacity, scale):
    """Add logo watermark to image"""
    h, w = image.shape[:2]
    logo_h, logo_w = logo.shape[:2]
    
    # Resize logo based on scale
    new_logo_w = int(logo_w * scale)
    new_logo_h = int(logo_h * scale)
    logo_resized = cv2.resize(logo, (new_logo_w, new_logo_h), interpolation=cv2.INTER_AREA)
    
    # Calculate position
    if position == 'top-left':
        x, y = 10, 10
    elif position == 'top-right':
        x, y = w - new_logo_w - 10, 10
    elif position == 'bottom-left':
        x, y = 10, h - new_logo_h - 10
    elif position == 'bottom-right':
        x, y = w - new_logo_w - 10, h - new_logo_h - 10
    else:  # center
        x, y = (w - new_logo_w) // 2, (h - new_logo_h) // 2
    
    # Ensure logo fits within image bounds
    if x < 0 or y < 0 or x + new_logo_w > w or y + new_logo_h > h:
        raise Exception("Logo too large for image")
    
    # Extract region of interest
    roi = image[y:y+new_logo_h, x:x+new_logo_w]
    
    # Blend logo with ROI
    blended = cv2.addWeighted(roi, 1 - opacity, logo_resized, opacity, 0)
    
    # Put blended region back
    result = image.copy()
    result[y:y+new_logo_h, x:x+new_logo_w] = blended
    
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            opacity = float(request.form.get('opacity', 0.5))
            position = request.form.get('position', 'bottom-right')
            scale = float(request.form.get('scale', 1.0))
            text = request.form.get('text', '')
            
            # Load main image
            image = None
            if 'image_file' in request.files and request.files['image_file'].filename:
                file = request.files['image_file']
                if file and allowed_file(file.filename):
                    img = Image.open(file.stream)
                    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            elif request.form.get('image_url'):
                url = request.form.get('image_url')
                image = download_image_from_url(url)
            
            if image is None:
                return render_template('index.html', error='Please provide an image file or URL')
            
            # Apply logo watermark if provided
            if 'logo_file' in request.files and request.files['logo_file'].filename:
                logo_file = request.files['logo_file']
                if logo_file and allowed_file(logo_file.filename):
                    logo_img = Image.open(logo_file.stream)
                    logo = cv2.cvtColor(np.array(logo_img), cv2.COLOR_RGB2BGR)
                    image = add_logo_watermark(image, logo, position, opacity, scale)
            
            # Apply text watermark if provided
            if text:
                image = add_text_watermark(image, text, position, opacity, scale)
            
            # Save result
            output_filename = f'result_{uuid.uuid4().hex}.png'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            cv2.imwrite(output_path, image)
            
            # Return page with result
            return render_template('index.html', 
                                 result_image=url_for('static', filename=f'output/{output_filename}'),
                                 success=True)
        
        except Exception as e:
            return render_template('index.html', error=f'Error processing image: {str(e)}')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
