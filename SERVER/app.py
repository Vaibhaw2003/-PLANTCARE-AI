from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import sqlite3
import os
from datetime import datetime

# -------------------------------
# App Setup
# -------------------------------

app = Flask(__name__)
CORS(app)

# -------------------------------
# Path Setup
# -------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "PUBLIC")
MODEL_PATH = os.path.join(BASE_DIR, "model", "plant_model.h5")
DB_PATH = os.path.join(BASE_DIR, "predictions.db")

# -------------------------------
# Load Model
# -------------------------------

model = tf.keras.models.load_model(MODEL_PATH)
classes = ["Healthy", "Powdery Mildew", "Rust", "Leaf Spot"]

# -------------------------------
# Initialize Database
# -------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT,
            confidence REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------
# Routes
# -------------------------------

# Serve Home Page
@app.route("/")
def home():
    return send_from_directory(PUBLIC_DIR, "index.html")

# Serve Static Files (CSS, JS, other pages)
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(PUBLIC_DIR, filename)

# -------------------------------
# Prediction API
# -------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Process Image
    img = Image.open(file).resize((10, 10))  # dummy model size
    img_array = np.array(img).flatten()
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    disease_name = classes[class_index]

    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (disease, confidence, date) VALUES (?, ?, ?)",
        (disease_name, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return jsonify({
        "disease": disease_name,
        "confidence": round(confidence * 100, 2)
    })

# -------------------------------
# Dashboard API (History)
# -------------------------------

@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "disease": row[1],
            "confidence": row[2],
            "date": row[3]
        })

    return jsonify(results)

# -------------------------------
# Run Server
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)