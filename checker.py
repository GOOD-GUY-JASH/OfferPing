from playwright.sync_api import sync_playwright
import json
import requests
import re

with open("products.json", "r") as f:
    products = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )

    page.set_default_timeout(60000)

    for product in products:
        print("=" * 60)
        print("Checking:", product["url"])

        try:
            page.goto(product["url"], wait_until="domcontentloaded")
            page.wait_for_timeout(5000)

            text = page.locator("body").inner_text()

            print("\n===== PAGE PREVIEW =====")
            print(text[:5000])
            print("========================\n")

            prices = re.findall(r"₹\s*([\d,]+)", text)

            if not prices:
                print("❌ No prices found")
                continue

            prices = [int(x.replace(",", "")) for x in prices]

            print("Prices:", prices)

            lowest = min(prices)

            print("Lowest:", lowest)

            if lowest <= product["target_price"]:
                print("🔥 Deal Found!")

                requests.post(
                    product["discord_webhook"],
                    json={
                        "content": f"🔥 Deal Found!\n₹{lowest}\n{product['url']}"
                    },
                    timeout=15
                )

            else:
                print("❌ Price above target")

        except Exception as e:
            print("ERROR:", e)

    browser.close()
