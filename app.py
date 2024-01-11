import io
import base64
from flask import Flask, render_template
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
    array = generate_image()
    image_data = array_to_base64_image(array)
    return image_data

def array_to_base64_image(array):
    array = np.uint8(array)
    image = Image.fromarray(array)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def generate_image():
    #C:/Users/shrey/PORTFOLIO_SITE
    generator = tf.keras.models.load_model("MODELS/human_face_generator.h5 ")
    noise = tf.random.normal(shape=(1, 100), mean=0.0, stddev=1.0)
    generated_image = generator(noise, training=False)[0]
    generated_image = generated_image * 127.5 + 127.5
    return generated_image

if __name__ == "__main__":
    app.run()
