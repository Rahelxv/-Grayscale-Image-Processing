from flask import Flask, request, send_file, render_template
from PIL import Image
import numpy as np
import os
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    img = Image.open(file.stream).convert('RGB')
    img_array = np.array(img)
    
    # Convert to grayscale using luminance formula
    r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray_uint8 = gray.astype(np.uint8)
    
    # Save grayscale image to a byte stream
    gray_img = Image.fromarray(gray_uint8)
    byte_io = io.BytesIO()
    gray_img.save(byte_io, 'JPEG')
    byte_io.seek(0)
    
    return send_file(byte_io, mimetype='image/jpeg', as_attachment=True, download_name='gray_image.jpg')

if __name__ == '__main__':
    app.run(debug=True)
