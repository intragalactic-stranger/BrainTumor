# Import all necessary packages
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
import absl.logging
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import cv2

# Ignoring all unnecessary warnings.
absl.logging.set_verbosity(absl.logging.ERROR)
tf.get_logger().setLevel("ERROR")

# Instantiate fastapi server.
app = FastAPI()

# Define links that CORS policy should allow.
origins = [
    "http://localhost",
    "http://localhost:3000"
]

# Add middleware to fastapi instance.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# To server the tensorflow model(s) using tensorflow serving;
# Visit (https://www.tensorflow.org/tfx/serving/setup) to see how to setup tensorflow serving with Docker Images
# After opening Docker Desktop and setting up tf serving, run the below line, preferably on Windows Powershell:
# `docker run -t --rm -p 8501:8501 -v C:/Users/ifunanyaScript/Everything/BrainTumour_DiagnosisApp:/BrainTumour_DiagnosisApp tensorflow/serving --rest_api_port=8501 --model_config_file=/BrainTumour_DiagnosisApp/model_configs/simple.config`

# This is the tf_serving link, We'll call the predict function of the model through this link. 
endpoint = "http://localhost:8501/v1/models/brain_tumour:predict"

# Note: This should correspond with the one in the notebooks. 
LABELS = ['no_tumour', 'tumour']


# @app.get("/awake")
# async def awake():
#     return "I am awake!!!"


def bytes_to_image(bytes) -> np.ndarray:
    image = np.array(Image.open(BytesIO(bytes)))
    return image

@app.post("/classify")
async def clasify(file: UploadFile = File(...)):
    # file.read returns a byte array which is converted to an image
    image = bytes_to_image(await file.read())
    # Resize the image because the model expects (224, 224)
    image = cv2.resize(image, (224, 224))

    # Create a batch.
    image_batch = np.expand_dims(image, 0)

    # Convert image to tf_serving data format.
    image_data = {
        "instances": image_batch.tolist()
    }

    # tf_serving response.
    response = requests.post(endpoint, json=image_data)

    # This gets the prediction array from the json response.
    prediction = response.json()["predictions"][0]

    predicted_label = LABELS[np.argmax(prediction)]
    confidence = np.max(prediction)

    return {
        "label": predicted_label,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
