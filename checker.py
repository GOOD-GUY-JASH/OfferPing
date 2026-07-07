from playwright.sync_api import sync_playwright
import json
import requests
import re

with open("products.json", "r") as f:
    products = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for product in products:
        print("Checking:", product["url"])

        page.goto(
    product["url"],
    wait_until="domcontentloaded",
    timeout=60000
        )

        text = page.locator("body").inner_text()

        prices = re.findall(r"₹\s?([\d,]+)", text)

        if not prices:
            print("No prices found")
            continue

        nums = [int(x.replace(",", "")) for x in prices]
        lowest = min(nums)

        print("Lowest price found:", lowest)

        if lowest <= product["target_price"]:
            requests.post(
                product["https://discord.com/api/webhooks/1523315799996235776/4ULytFxdpqKQZdLCQsgBLnFy7l6MW1yzVFVFoC1PoZnYhHnN3F46h2Bm6WbyJtON-WLS"],
                json={
                    "content": f"🔥 Deal Found!\nPrice: ₹{lowest}\n{product['url']}"
                }
            )

    browser.close()
