from playwright.sync_api import sync_playwright

url = "https://dl.flipkart.com/dl/hp-victus-intel-core-i5-14th-gen-14450hx-24-gb-512-gb-ssd-windows-11-home-6-graphics-nvidia-geforce-rtx-4050-15-fa2382tx-gaming-laptop/p/itmc8b9497c77521"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    print(page.title())
    browser.close()
