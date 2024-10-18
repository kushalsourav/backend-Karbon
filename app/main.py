from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS
from .model import probe_model_5l_profit

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file and file.filename.endswith(".json"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        try:
            with open(filepath, "r") as f:
                content = f.read()

                data = json.loads(content)

            result = probe_model_5l_profit(data["data"])

            return jsonify(result), 200

        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400

    else:
        return jsonify({"error": "Invalid file type, only JSON is allowed"}), 400
