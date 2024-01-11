import io
import base64
from flask import Flask, render_template, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
import os
app = Flask(__name__, static_url_path='', static_folder='templates')

@app.route('/')
def index():
    array = generate_image()
    image_data = array_to_base64_image(array)
    return render_template('index.html', image_data=image_data)

@app.route('/generate')
def generate():
    generated_image, noise = generate_image()
    generated_data = array_to_base64_image(generated_image)
    noise_data = array_to_base64_image(noise)
    return jsonify({'image_data': generated_data, 'noise_data': noise_data})

def array_to_base64_image(array):
    print(array)
    array = np.array(array)
    normalized_array = (array - np.min(array)) / (np.max(array) - np.min(array)) * 255.0
    array = np.uint8(normalized_array)
    array = np.uint8(array)
    image = Image.fromarray(array)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def generate_image():
    generator = tf.keras.models.load_model("C:/Users/shrey/PORTFOLIO_SITE/MODELS/human_face_generator.h5 ")
    noise = tf.random.normal(shape=(1, 100), mean=0.0, stddev=1.0)
    generated_image = generator(noise, training=False)[0]
    generated_image = generated_image * 127.5 + 127.5
    noise_reshaped = tf.reshape(noise, [10, 10])
    return generated_image, noise_reshaped

if __name__ == "__main__":
    app.run()
