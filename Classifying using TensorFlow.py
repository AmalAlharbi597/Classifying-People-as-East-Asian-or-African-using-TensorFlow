# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VX-59xi1RIjP0iqFYpxc88ynZcxWOY3K
"""

from google.colab import files


print("Upload the saved model folder (as a .zip file):")
model_file = files.upload()

print("Upload the image to classify:")
image_file = files.upload()

import zipfile
import os


model_zip_path = list(model_file.keys())[0]
output_folder = "/content/converted_savedmodel"

with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
    zip_ref.extractall(output_folder)

print(f"Model extracted to: {output_folder}")

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Paths for the model and the image
model_path = "/content/converted_savedmodel/model.savedmodel"  # Path to the model
image_path = "/content/pred.jpg"  # Path to the image

# Class names (replace with actual class names from your model)
class_names = ["African people", "East Asian people"]

try:
    # Load the model using tf.saved_model.load
    model = tf.saved_model.load(model_path)
    print("Model loaded successfully!")

    # Access the default signature of the model
    signature = model.signatures["serving_default"]

    # Display the available output names
    print("Available outputs:")
    print(signature.structured_outputs)

    # Preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))  # Resize the image to match the input size
    img_array = image.img_to_array(img)  # Convert the image to a NumPy array
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Add a batch dimension and normalize the values

    # Predict using the default signature
    predictions = signature(tf.constant(img_array))
    logits = predictions["sequential_3"]  # Use the correct output name from your model
    predicted_class = np.argmax(logits.numpy())  # Determine the predicted class
    confidence = logits.numpy()[0][predicted_class]  # Get the confidence score for the predicted class

    # Display the results
    print(f"Predicted Class: {class_names[predicted_class]}")
    print(f"Confidence: {confidence * 100:.2f}%")
except Exception as e:
    print(f"An error occurred: {e}")