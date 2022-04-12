import io, base64
from PIL import Image

from glob import glob
from operator import index
from flask import Flask, jsonify, request

app = Flask(__name__)

global selectedLetters, selectedIndecies

selectedLetters = ["E","N","G","I","R"]
selectedIndecies = [1, 1, 2, 0, 0]    # Keeps track of what state each letter prompt is in. 
                                                        # (true - guessed correctly, false - guessed incorrectly, 
                                                        # first false - pending)

@app.route("/", methods=["GET"])
def sign_in():
    return jsonify({"hello": "world"})

@app.route("/getState", methods=["GET"])
def get_letters():
    global selectedIndecies
    return jsonify({
        "selectedLetters": selectedLetters,
        "selectedIndecies": selectedIndecies
    })


@app.route("/clearState", methods=["POST"])
def clear_letters():
    global selectedIndecies
    selectedIndecies = [2,0,0,0,0]
    return jsonify({
        "selectedLetters": selectedLetters,
        "selectedIndecies": selectedIndecies
    })

@app.route("/makeGuess", methods=["POST"])
def guess_letter():
    global selectedIndecies
    base64String = request.form.to_dict()["base64Image"]

    # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64String, "utf-8"))))
    img.save('testImage.jpeg')

    # test image in ML get back a confidence and then adjust state...
    # will just say its correct to test the rest of the API
    guess = True

    if(guess):
        
        index = selectedIndecies.index(2)
        if(index < len(selectedIndecies) -1):
            selectedIndecies[index] = 1
            selectedIndecies[index+1] = 2
        else:
            clear_letters()
    return jsonify({
        "selectedLetters": selectedLetters,
        "selectedIndecies": selectedIndecies
    })

if __name__ == "__main__":
    app.run(debug= True)