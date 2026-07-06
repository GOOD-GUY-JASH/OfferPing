from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/track", methods=["POST"])
def track():
    data = request.json

    if os.path.exists("products.json"):
        with open("products.json", "r") as f:
            products = json.load(f)
    else:
        products = []

    products.append(data)

    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

    return jsonify({"message": "Product added!"})

@app.route("/products")
def products():
    with open("products.json", "r") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
