from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_letters():
    return jsonify({"hello": "test"})

@app.route("/test", methods=["GET"])
def set_letters():
    return jsonify({"test": "test2"})

if __name__ == "__main__":
    app.run(debug= True, ssl_context='adhoc')