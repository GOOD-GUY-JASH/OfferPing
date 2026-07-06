from flask import Flask, request, jsonify

app = Flask(__name__)

products = []

@app.route("/")
def home():
    return {
        "status": "online",
        "app": "OfferPing",
        "version": "1.0"
    }

@app.route("/save-product", methods=["POST"])
def save_product():
    data = request.get_json()

    products.append({
        "url": data.get("url"),
        "target_price": data.get("target_price")
    })

    return jsonify({
        "success": True,
        "message": "Product saved!"
    })

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
