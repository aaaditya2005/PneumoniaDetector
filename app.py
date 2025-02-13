import gdown
import os
import tensorflow as tf
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

MODEL_FILE_ID = "1HjQA4_c6YFp4bxJnMD1CnLU68Xt-3MEF"
MODEL_PATH = "model/v2.h5"

if not os.path.exists(MODEL_PATH):
    url = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(150, 150), color_mode='grayscale')
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    img_array = img_array / 255.0

    prediction = model.predict(img_array)
    result = 'Pneumonia' if prediction[0] > 0.5 else 'Normal'

    return render_template('result.html', result=result, img_path=filepath)

if __name__ == '__main__':
    app.run(debug=True)
