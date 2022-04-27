import io, base64
from PIL import Image

from glob import glob
from operator import index
from flask import Flask, jsonify, request

import tensorflow as tf
from tensorflow import keras
import numpy as np

app = Flask(__name__)

global selectedLetters, selectedIndecies

letterSet = ["E","N","G","I","R"]
currLetter = 0   # Keeps track of letter state -1 means no letter gotten

img_height = 224
img_width = 224
class_names = ['E', 'G', 'I', 'N', 'R']  # Different order of letters for clasiffier

# load model
sign_model = tf.keras.models.load_model('ASL_MODEL_V1.h5')


@app.route("/", methods=["GET"])
def sign_in():
    return jsonify({"hello": "world"})

@app.route("/getState", methods=["GET"])
def get_letters():
    global letterSet, currLetter
    return jsonify({
        "letterSet": letterSet,
        "currLetter": currLetter
    })


@app.route("/clearState", methods=["POST"])
def clear_letters():
    global letterSet, currLetter
    currLetter = 0
    return jsonify({
        "letterSet": letterSet,
        "currLetter": currLetter
    })

@app.route("/makeGuess", methods=["POST"])
def guess_letter():
    global letterSet, currLetter
    base64String = request.form.to_dict()["base64Image"]

    # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64String, "utf-8"))))
    img.save('testImage.jpg')

    img = tf.keras.utils.load_img(
    "./testImage.jpg", target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = sign_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

    guess = False

    if letterSet[currLetter] == class_names[np.argmax(score)]:
        guess = True    

    if(guess):
        if currLetter < len(letterSet):
            currLetter = currLetter + 1
        else:
            currLetter = 0
    return jsonify({
        "letterSet": letterSet,
        "currLetter": currLetter
    })

if __name__ == "__main__":
    app.run(debug= True)