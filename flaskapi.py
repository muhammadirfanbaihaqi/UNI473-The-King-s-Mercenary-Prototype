from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # agar bisa diakses dari luar seperti Streamlit

# Simpan data terakhir
data_terakhir = {
    "suhu": None,
    "pakan": None,
    "pompa": None,
    "timestamp": None
}

@app.route("/sensor", methods=["POST"])
def sensor():
    global data_terakhir
    data = request.json
    print("Data diterima:", data)

    data_terakhir = {
        "suhu": data.get("suhu"),
        "pakan": data.get("pakan(%)"),
        "pompa": data.get("pompa"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify({"status": "sukses", "data": data_terakhir}), 200

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data_terakhir)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
