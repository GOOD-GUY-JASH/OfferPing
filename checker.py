import json

with open("products.json", "r") as f:
    products = json.load(f)

print(products)
