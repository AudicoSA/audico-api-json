
import json
import os
from difflib import get_close_matches

# Load product data once
with open(os.path.join(os.path.dirname(__file__), '../products.json')) as f:
    PRODUCTS = json.load(f)

def handler(request, response):
    try:
        query = request.args.get("query", "").lower()
        results = []

        for product in PRODUCTS:
            name = product["name"].lower()
            sku = product["sku"].lower()

            if query in name or query in sku:
                results.append(product)

        if not results:
            names = [p["name"] for p in PRODUCTS]
            close_matches = get_close_matches(query, names, n=5, cutoff=0.3)
            results = [p for p in PRODUCTS if p["name"] in close_matches]

        return response.json(results[:10])
    except Exception as e:
        return response.status(500).json({ "error": str(e) })
