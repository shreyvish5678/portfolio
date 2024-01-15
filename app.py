import io
import base64
from flask import Flask, render_template, jsonify
import warnings
import tensorflow as tf
from PIL import Image
import numpy as np
app = Flask(__name__, static_url_path='', static_folder='templates')
warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")
@app.route('/')
def index():
    noise = generate_noise()
    array = generate_image(noise)
    noise = normalize_to_0_255(noise)
    image_data = array_to_base64_image(array)
    noise_data = array_to_base64_image(noise)
    return render_template('index.html', image_data=image_data, noise=noise_data)

@app.route('/generate')
def generate():
    noise = generate_noise()
    array = generate_image(noise)
    noise = normalize_to_0_255(noise)
    image_data = array_to_base64_image(array)
    noise_data = array_to_base64_image(noise)
    return jsonify({"image_data": image_data, "noise": noise_data})

def array_to_base64_image(array):
    array = np.uint8(array)
    image = Image.fromarray(array)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def generate_image(noise):
    noise = tf.reshape(noise, shape=(1, 100))
    generator = tf.keras.models.load_model('MODELS/human_face_generator.h5')
    generated_image = generator(noise, training=False)[0]
    generated_image = generated_image * 127.5 + 127.5
    return generated_image

def normalize_to_0_255(tensor):
    min_value = np.min(tensor)
    max_value = np.max(tensor)
    normalized_tensor = (tensor - min_value) / (max_value - min_value) * 255
    return normalized_tensor

def generate_noise():
    noise = tf.random.normal(shape=(10, 10), mean=0.0, stddev=1.0)
    return noise

if __name__ == '__main__':
    app.run(debug=True)