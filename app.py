import os
import uuid
from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

SCREENSHOT_DIR = "static/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

URL_ALIASES = {
    "Seznam – homepage": "https://seznam.cz",
    "Google": "https://google.com",
    "IDNES": "https://idnes.cz",
    "Mall – produkce": "https://mall.cz"
}

DEVICE_PROFILES = {
    "iPhone 12": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPad Air": {"viewport": {"width": 820, "height": 1180}, "scale": 2, "mobile": True},
    "Samsung S23": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Desktop HD": {"viewport": {"width": 1920, "height": 1080}, "scale": 1, "mobile": False},
}

@app.route("/")
def index():
    return render_template("index.html",
                           devices=list(DEVICE_PROFILES.keys()),
                           aliases=URL_ALIASES)

@app.route("/run_test", methods=["POST"])
def run_test():
    url = request.form.get("url")
    device = request.form.get("device")

    profile = DEVICE_PROFILES.get(device)
    if not profile:
        return "❌ Neznámé zařízení"

    screenshot_name = f"screenshot_{uuid.uuid4()}.png"
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport=profile["viewport"],
                device_scale_factor=profile["scale"],
                is_mobile=profile["mobile"]
            )
            page = context.new_page()
            page.goto(url, timeout=30000)
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()

        return f"""
        ✅ Screenshot hotový!<br>
        <a href='/static/screenshots/{screenshot_name}' target='_blank'>Otevřít obrázek</a>
        """
    except Exception as e:
        return f"❌ Chyba během testu: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)