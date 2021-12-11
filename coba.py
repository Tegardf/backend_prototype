import cv2
import pytesseract
import base64
import numpy as np
from flask import Flask,render_template,request
from flask_cors import CORS
from gtts import gTTS
from io import BytesIO
from pytesseract import Output
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data_img = request.json['value_base64']
    data_with_padding = f"{data_img}{'=' * ((4 - len(data_img) % 4) % 4)}"
    PIL_image = Image.open(BytesIO(base64.b64decode(data_with_padding)))
    # print(data_img)
    return PIL_image

if __name__ == "__main__":
    app.run(debug=True)