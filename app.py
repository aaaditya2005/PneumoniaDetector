from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

model = tf.keras.models.load_model('model/v2.h5')

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
