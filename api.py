from operator import index
from flask import Flask, jsonify

app = Flask(__name__)

selectedLetters = ["E","N","G","I","R"]
selectedIndecies = [1, 1, 2, 0, 0]    # Keeps track of what state each letter prompt is in. 
                                                        # (true - guessed correctly, false - guessed incorrectly, 
                                                        # first false - pending)

@app.route("/", methods=["GET"])
def sign_in():
    return jsonify({"hello": "world"})

@app.route("/getState", methods=["GET"])
def get_letters():
    return jsonify({
        "selectedLetters": selectedLetters,
        "selectedIndecies": selectedIndecies
    })

if __name__ == "__main__":
    app.run(debug= True)