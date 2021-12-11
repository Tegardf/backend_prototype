from gtts import gTTS
import cv2
import pytesseract
import base64
import numpy
import secrets
from io import BytesIO
from pytesseract import Output
from flask_cors  import CORS,cross_origin
from PIL import Image
from flask import Flask,render_template, request
from werkzeug import debug

# host = "0.0.0.0"
# port = 5000

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)
# api_v1_cors_config = {
#     "origins":["*"],
#     "methods":["GET","POST","OPTIONS"]
# }
# CORS(app,resource={
#     r"/submit" : api_v1_cors_config
# })
# cors = CORS(app , resources={r"/submit": {"origins": "http://localhost:3000/"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
# @cross_origin()
def home():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
# @cross_origin()
def submit():
    PIL_image = get_image()
    image = cv2.cvtColor(numpy.array(PIL_image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #gray image
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    custom_config = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')
    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
        if int(float(details['conf'][sequence_number])) >30:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
            threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    last_word = ''
    myText = ""
    for word in details['text']:
        if word!='':
            myText += ' ' + word
            last_word = word
        if (last_word!='' and word == '') or (word==details['text'][-1]):
            myText += '\n'
    language = 'en'
    output = gTTS(text=myText, lang=language, slow=False)
    fp = BytesIO()
    output.write_to_fp(fp)
    fp.seek(0)
    audio_content = base64.b64encode(fp.getvalue())
    audio_output = audio_content.decode('UTF-8')
    # print("hi")
    # response.header.add('Access-Control-Allow-Origin', 'http://localhost:3000/')
    # response = {
    #     'audio_out':audio_content,
    #     'text_out':myText
    # }
    return "test"

# @cross_origin()
def get_image():
    data_img = request.json['value_base64']
    # data_img = 'UklGRrQKAABXRUJQVlA4TKgKAAAvToGBAA8w//M///MfeByBQNL+5BtERNKD3FrbmzEZxKQ1MjUTeAyXZL4N6NMeVEbkUDFAEpnKqLMKHekW309s3UT0fwJsT9vvto0jDT2LLVohPS6KqDTpsmEmFmOaSE+2UbntkUe75I2LLKSIESNIYWaV4siFKcQYIv6F9Wz1hF6Ryx3JzGKJlCuPHYoaKkSKZwT7TEyc0RF/FzgADpCuvYno/wRMFVPD0gkGhUll0QR2qSaahR4wCswKqyF0AVVucpeHPOUFkQqWStAodCqDxqSzuB4WSkAt0Cr0BqPDHAi3IEoqNdWG3jpGH5hj4pa3hgMHpkOHVowYocwyi7rqqvbsaR6E//eIVXv66dSbndv7V9e/+3Hn0oWXr7/eP/0/xL+S2Kj9Qx0PyRu1HfXdoXjihTdqF9T3h+JUsfxIQj0UiieKN2vy2ufCoHylWKsdV54OAf/G2lLt9ko1DAH+v8qMZpu9qGWUOSQtkrh9D0/3dGfrFyPmPeyLny/3tlrGUgRJWTJg38uUexZnVy9G2oj4MqVV3GoZcezQYTummaK8elHaaflrzRTx9rZDiDuORE1Rfn4F7aS7vlC6iCvbRvweEibJBagpoinKD7FaxbVtI15FQowMdH+iiKacHV5BOzwwKPfWdowBDgkKiduKIpowO5yX2kyay8qOsRRFQp4QO+aYSV2JtDUWday8aVjyfSFvE0RJp95TNRm0Zur4yIZB5PtC1SYoczjqOIxYmFIRx+oGkduxTUxQZlIzId2eZMH1zRd7Y4ZBerlJE/fZeL5sirPtOOJUfwNZ2jIfN3EfwbhpivNswniARyQc4QhHOJuzOZuzeZu3eZu3eYu3eIu3olbUilJCewBABgACZlBmYDlx0qZtO5zMBFFALhgApiOnmlZ2+txQ34/ivkQt72I6Ts+c1ncSM+cu/PzadQa/7rgAAGSlZOPZRPpcvRZTGOSRp1kpWTxNu+pLE8csTzNSstgnUqq+DEDI05SUbDAzvWAAOCcldVWcSdVrMdMXQhh7mpaSTVWenmbSOxEnNFe5qwHVH92HQUNhaNHs4AI/uCI6EIARQCUwQ5y3aWsuVCabmoBoGgaA6WZzaHl2zIrwg3Xipwp5b6fbTyfGvzvcnmnrT3f9GKB0aFsAANmpZCI2MrKL2juPgy+54GI4Zqc+lYiNDO2inZ2f+IO8i+mYmVpMxEZExyMBIMdU0qW980yXAaJhDADn2tlELJ3YnWnrur8/Ci5LjulmcyyWHtuN8IN14uu98zaNKkPg/+JCeOBHC0fFiwjQYWD0Lto01QdisCmLiKZhAFi+0Tv2rvsDfVKZQVXUXAzHhRvjwkY7kR5GDIx1rUOrAgCoN2LHzWcTnX4mmpvm4XSCWw1Ln9i5yMRgY/KMEK2IAeCCEjtuqqKZYmIKLmXH8rJD7pvbYCLZNK8aBOnHCFErRMEejDIcJAhenLRpm4GZooBcMAD0Dez0lfn4QN/zkedzfpCWd/mjQ79p6oWL12/9+bggYD972q87tFvgqJn6mrF3yxRPxHxFtDyi/YlyxCEcXuWE3pafcXHMot2hZHb0NSOfiU/k8EU/C12EaD0U7LiNf/BJhDV2W9hhP6uvXVRwdiIi+RIQxp76+vr1NX7g8KFIhqv4WRHihEY1AAAMAIBMF9gyiUF4coGF8ECLFtSyY9+xq7IxRNtl30EcJmGzuY7cMIBcfiw+0B+5VI6wqII3uPMTpZZqqwWFheGhAgCg1mo1c0ctMdpz0ShvP3aYY4e9lfS3xLaplqpsiLe4XoMdUy1hJnLXZQ0DQHZV2XuzrZaWmQjgUnGc748/3L96uXSSyXstF6psADXOgu5BdFFDcNFlOQQhPCi0BVogOR8qgwhkbdo9TwCEARLjiIYxAPRMDtyUGrO/O3Wpspzzp7oQR+G6kt+rp+68rSox7AvUDq0MAKDuKXmspxuGWvKX81CgnCi8iO9ONypqKdbyI3ooUa4qAnku1dDVUuyiH9nDDcptRSCn0o26WoppDBBNwY6ritQ9n2roquLvBIq7VCnHClJXmm6UL1diFT85lLVp7nIXAvUmQnguhijoAywI5K7clu0Alnx1fRkrsk3TfHRl8L0piMgFA0C5urwgvJZtnkqNEV/VBc3FcBSU8QVJkOtPp1Lg21jQOi4AAGoptoAEOZkcTjPIFF1MRymeWRBekJOfGp4Ox4tycnFYZrDg1nGopdhCnp2GaAgDQEEZF168Jm98PbXIQBBc9hzl6nJEeEFufjo1y2BFsmlUAhgC/hcXwgNABkx1A6s4CNRhqg2wziIqTto0hSJ3wTABNDYCoq1hx9DN8tQPtycenvtVxRev5V1qlFRdn2rrJUVqK75GtF93aFVwnKs3ptoNclVqq76Oa3lE+wllul6capcTBenBki9BHLNoqiN72tEdvCo9IL5igBCtRDnrIEUmvV23AnakHHeKivAA+xIRxrSKY6l5szi1WklMPvSg4k+IE1pY3wEhkgiJ2JzN2ZzN2ZzN2ZzNW7zFW7zFW7zFW3wz2nWE9n8AYnj4SQpmtyLP2zTjXlCCKCAXIVdtNspNdgta3m3kN1hvFHAQv+647WUbjVIAmaKXaoguBhP9vhdhPRhY0PLIZVy7petBCILgwk/mqs1yqcVuRZq3aWH9XwsOCWdvBRNdEd9l0UQISlgH5BLtzwXCZ7wY+tVARjLrgF12a+uBHBcStpdcIEIEEPFwLZCY7O16IL0JQF0X444SiKi9KLlFB3PBVIV5oIX1HSfrDiMEvA3rwIXDwLAO50NyYuA1hHOVchiuH3kR7189vxECnigvErKeMUJgxApCl+TCkVcEQq6F44/Ki/v4ejgU5UV8XslshIA/XHgRRXK4HIKw/rciiusa7BNCTLODxHVNC2Yd9vcpnYD4nkOH4kNDPVbv0tISd+hQT5edKEY1sAkhptlCYlTTgF10cJCH+fl5u1ptbUcHeT6ArW8mk4tzcwv49lu12reSZ0cDCOs7ySqRd5FcTjYVc3SlNdv1xo8ZTU8XWjoIgrx5xEy/UvsEeBdHkl1xFVo2TW3pIM0lNg+3vjfxxLCvL3S1j8ET92mlmr4lzb2+ebiF5gcuMmg8t/uNDi1e6ytKc8WV9/yWyfusO6fqHzJppZoO0lyRO/qXvUzC8PXl7tZz8I0OTV1yNEau3MQs3u3tgqpvCYIxktf3WRzpFj+2+8R92rY6qOZyu8f/qO/vv77lQ35VacZXjZZNC+sBM5FwhCMc4WzO5mzO5m3e5m3e5i3e4i3eilpRK0oJ7f+2TADDwQMAAQDEjmu67HoQWYmmi+kCAXD9/Xp8arae227mytXliDA7xGzzjv704tlU3dRtXFDGhYmUxMzcv/vM4vC5ulkkuHQyI02MfI/d43cfAVqrdDIzNzEisXv77iMwRrlISc+y+/PdJ7o0rXQyI02kgd2ZuzWSSW2YOtFKyrgwkR5i9/jdGs5YZXObVErV5YgwMsKKjsEVI1jfDYZ4Es1AxK4n2QokyKNO+6bqg6VFC3rphVFHZbbZWH11EYiAUqBWaA16hzFgzuRhippKS7WnNlKfaawoJqrc5C4PecoLAt7LPyE6lAF1QltwWSxVbnKXhzzlBYGLc2NurBQbZaNutI1d'
    data_with_padding = f"{data_img}{'=' * ((4 - len(data_img) % 4) % 4)}"
    return Image.open(BytesIO(base64.b64decode(data_with_padding)))

#start server & app
if __name__ == "__main__":
    app.run(debug=True)