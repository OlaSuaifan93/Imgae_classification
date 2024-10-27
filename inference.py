#import libraries for array manipulation, ONNX model runtime, image processing and HTTP request
import numpy as np
import onnxruntime as ort
from PIL import Image
import requests
from io import BytesIO

# Load the model initializes an ONNX runtime session with the specified model path
model_path = 'resnet50.onnx'
session = ort.InferenceSession(model_path)

# preprocess image by a function via:
def preprocess_image(image_url):
    response = requests.get(image_url) #1. download the image from a url
    img = Image.open(BytesIO(response.content))
    img = img.resize((224, 224))  # 2. Resize to model input size expected by the model (224x224 for ResNet)
    img = np.array(img).astype(np.float32)  # 3. Convert image to numpy array and normalizes pixel values to the range [0,1]
    img = np.transpose(img, (2, 0, 1))  # 4. rearrange the dimensions from HWC to CHW (channel, height, width) for compatability with the model
    img = img / 255.0  # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0)  # 5. expand dimensions to add batch size (required for the model input)
    return img

# Image URL for testing
image_url = 'https://www.thesprucepets.com/thmb/kDcQES0eO7DnfjZ5CBmkfOrxnyg=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/facts-about-siamese-cats-4173491-hero-5a607df9e57b40a58c803a76859b6694.jpg'
input_data = preprocess_image(image_url)

# Run inference prepares input data and runs inference on the model, capturing the output
inputs = {session.get_inputs()[0].name: input_data}
output = session.run(None, inputs)

# Output the results
print("Output:", output)
