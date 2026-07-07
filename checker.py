from playwright.sync_api import sync_playwright
import json
import requests
import re

# Load products
with open("products.json", "r") as f:
    products = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()
    page.set_default_timeout(60000)

    for product in products:
        print("=" * 50)
        print("Checking:", product["url"])

        try:
            page.goto(product["url"], timeout=60000)

            text = page.locator("body").inner_text()

            prices = re.findall(r"₹\s*([\d,]+)", text)

            if not prices:
                print("❌ No prices found")
                continue

            prices = [int(price.replace(",", "")) for price in prices]

            print("All prices found:", prices)

            lowest = min(prices)

            print("Lowest price:", lowest)

            if lowest <= product["target_price"]:
                print("🔥 Deal Found!")

                requests.post(
                    product["discord_webhook"],
                    json={
                        "content": (
                            f"🔥 **OfferPing Alert**\n\n"
                            f"💰 Current Price: ₹{lowest}\n"
                            f"🎯 Target Price: ₹{product['target_price']}\n"
                            f"🔗 {product['url']}"
                        )
                    }
                )

        except Exception as e:
            print("Error:", e)

    browser.close()
