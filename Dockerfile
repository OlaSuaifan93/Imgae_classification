# Base image with Python
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the ONNX model and script into the container
COPY resnet50.onnx .
COPY inference.py .

# Install the required Python libraries
RUN pip install onnxruntime numpy pillow requests

# Command to run the inference script when the container starts
CMD ["python", "inference.py"]

RUN pip install Flask
CMD ["python", "app.py"]
