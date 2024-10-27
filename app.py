from flask import Flask, request, jsonify
import numpy as np
import onnxruntime as ort
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load ONNX model
model_path = 'resnet50.onnx'
session = ort.InferenceSession(model_path)

def preprocess_image(image):
    img = image.resize((224, 224))  # Resize image
    img = np.array(img).astype(np.float32)  # Convert to numpy array
    img = np.transpose(img, (2, 0, 1))  # Change data layout
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image = Image.open(BytesIO(file.read()))
    input_data = preprocess_image(image)

    inputs = {session.get_inputs()[0].name: input_data}
    output = session.run(None, inputs)

    return jsonify({'prediction': str(output)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
