import io, base64
from multiprocessing.sharedctypes import Value
import random
from PIL import Image
import datetime

from glob import glob
from operator import index
from flask import Flask, jsonify, request, send_from_directory

import tensorflow as tf
from tensorflow import keras
import numpy as np

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import werkzeug

app = Flask(__name__)

global selectedLetters, selectedIndecies

# Folder paths for google drive
folderIDs = {
            "E": '1O2U1TNVKJsp-OegBNGhx1OdwzwNZk9MS', 
            "N": '1Dtnxl49VY_jm_sxs3StN-UR8yYSDl3R9', 
            "G": '12UPEM8dlap-66JlLdVEF95z5kZ_bycn7', 
            "I": '1WU5CEWAQhfDD7PIDYfy3mMmILKNdZdLw', 
            "R": '1q0GvikjqHZl3rsOVSXq-r-i_GMAyqFd3'
            }

letterSet = ["E","N","G","I","R"]
wordSet = {
    "hard": ["ENGINEERING", "ENGINEER", "REIGN"],
    "medium": ["RINE", "GRIN", "RING"],
    "easy": ["RIG", "EGG", "ENG"]
}

# score dictionary
scores = [
    {"name": "test", "score": 10}
]

img_height = 224
img_width = 224
class_names = ['E', 'G', 'I', 'N', 'R']  # Different order of letters for clasiffier

# load model
sign_model = tf.keras.models.load_model('ASL_MODEL_V1.h5')

# start google drive connection
gauth = GoogleAuth()           
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# add favicon so warning isnt there
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/", methods=["GET"])
def sign_in():
    return jsonify({"hello": "world"})

@app.route("/getScores", methods=["GET"])
def get_scores():
    scores = []
    scoreFile = open("scores.txt","r")

    for line in scoreFile.readlines():
        if(line):
            name = line.split(":")[0]
            score = line.split(":")[1].replace("\n", "")
            scores.append({"name": name, "score": int(score)})

    scoreFile.close()

    return jsonify({
        "scores": scores,
    })

@app.route("/addScore", methods=["POST"])
def add_score():
    name = request.form.to_dict()["name"].replace(":", "").replace("\\", "") # just for a little bit of safety
    try:
        score = int(request.form.to_dict()["score"].replace(":", "").replace("\\", ""))

        scoreFile = open("scores.txt","a")
        scoreFile.write(f"{name}:{score}\n")
        scoreFile.close()
    except ValueError:
        return jsonify({
            "error": 200,
            "description": "Name or score supplied is incorrect type."
        })

    return get_scores()

@app.route("/getLetterSet", methods=["GET"])
def get_letters():
    global letterSet
    return jsonify({
        "letterSet": letterSet,
    })

@app.route("/getWordSet", methods=["POST"])
def get_word():
    global wordSet
    difficulty = request.form.to_dict()["difficulty"]

    return jsonify({
        "word": wordSet[difficulty][random.randint(0, len(wordSet[difficulty])-1)],
    })

@app.route("/predictLetter", methods=["POST"])
def guess_letter():
    base64String = request.form.to_dict()["base64Image"]
    letter = request.form.to_dict()["currLetter"]

    # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64String, "utf-8"))))
    img.save('testImage.jpg')

    img = tf.keras.utils.load_img(
    "./testImage.jpg", target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # save to google drive
    gfile = drive.CreateFile({'parents': [{'id': folderIDs[letter]}]})

    gfile.SetContentFile("testImage.jpg")
    gfile['title'] = letter + str(datetime.datetime.now()) + '.jpg'
    gfile.Upload() # Upload the file.

    predictions = sign_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

    return jsonify({
        "letterPredicted": class_names[np.argmax(score)],
        "confidence": 100 * np.max(score)
    })

if __name__ == "__main__":
    app.run(debug= True)