import os
import uuid
from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

SCREENSHOT_DIR = "static/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ✅ Předdefinované URL
URL_ALIASES = {
    "Mall – produkce": "https://mall.cz",
    "Seznam": "https://seznam.cz",
    "Google": "https://google.com",
    "iDnes": "https://idnes.cz"
}

# ✅ VELKÝ SEZNAM ZAŘÍZENÍ – 70+ zařízení
DEVICE_PROFILES = {

    # ======= ✅ APPLE – iPhone =======
    "iPhone SE (2022)": {"viewport": {"width": 375, "height": 667}, "scale": 2, "mobile": True},
    "iPhone 11": {"viewport": {"width": 414, "height": 896}, "scale": 2, "mobile": True},
    "iPhone 12": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPhone 12 Pro Max": {"viewport": {"width": 428, "height": 926}, "scale": 3, "mobile": True},
    "iPhone 13 Mini": {"viewport": {"width": 375, "height": 812}, "scale": 3, "mobile": True},
    "iPhone 13": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPhone 13 Pro Max": {"viewport": {"width": 428, "height": 926}, "scale": 3, "mobile": True},
    "iPhone 14": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPhone 14 Plus": {"viewport": {"width": 428, "height": 926}, "scale": 3, "mobile": True},
    "iPhone 14 Pro": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 14 Pro Max": {"viewport": {"width": 430, "height": 932}, "scale": 3, "mobile": True},
    "iPhone 15": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 15 Pro": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 15 Pro Max": {"viewport": {"width": 430, "height": 932}, "scale": 3, "mobile": True},

    # ======= ✅ APPLE – iPad =======
    "iPad Mini": {"viewport": {"width": 768, "height": 1024}, "scale": 2, "mobile": True},
    "iPad Air": {"viewport": {"width": 820, "height": 1180}, "scale": 2, "mobile": True},
    "iPad Pro 11": {"viewport": {"width": 834, "height": 1194}, "scale": 2, "mobile": True},
    "iPad Pro 12.9": {"viewport": {"width": 1024, "height": 1366}, "scale": 2, "mobile": True},

    # ======= ✅ SAMSUNG =======
    "Samsung Galaxy S20": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Samsung Galaxy S21": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Samsung Galaxy S21 Ultra": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Samsung Galaxy S22": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung Galaxy S22 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung Galaxy S23": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung Galaxy S23 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung Galaxy S24": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung Galaxy S24 Ultra": {"viewport": {"width": 1440, "height": 3120}, "scale": 3, "mobile": True},

    # Foldables
    "Samsung Galaxy Fold": {"viewport": {"width": 1536, "height": 2152}, "scale": 3, "mobile": True},
    "Samsung Galaxy Z Flip": {"viewport": {"width": 1080, "height": 2636}, "scale": 3, "mobile": True},

    # Tablets
    "Samsung Tab S6": {"viewport": {"width": 1600, "height": 2560}, "scale": 2, "mobile": True},
    "Samsung Tab S8": {"viewport": {"width": 1600, "height": 2560}, "scale": 2, "mobile": True},

    # ======= ✅ GOOGLE =======
    "Google Pixel 5": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Google Pixel 6": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Google Pixel 6 Pro": {"viewport": {"width": 1440, "height": 3120}, "scale": 3, "mobile": True},
    "Google Pixel 7": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Google Pixel 7 Pro": {"viewport": {"width": 1440, "height": 3120}, "scale": 3, "mobile": True},
    "Google Pixel 8": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Google Pixel 8 Pro": {"viewport": {"width": 1344, "height": 2992}, "scale": 3, "mobile": True},

    # ======= ✅ XIAOMI =======
    "Xiaomi Mi 11": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Xiaomi 12": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Xiaomi 13": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},

    # ======= ✅ HUAWEI / ONEPLUS =======
    "Huawei P40": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "OnePlus 9": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "OnePlus 10 Pro": {"viewport": {"width": 1440, "height": 3216}, "scale": 3, "mobile": True},

    # ======= ✅ DESKTOP / LAPTOP =======
    "MacBook Air 13": {"viewport": {"width": 1440, "height": 900}, "scale": 2, "mobile": False},
    "MacBook Pro 14": {"viewport": {"width": 1512, "height": 982}, "scale": 2, "mobile": False},
    "MacBook Pro 16": {"viewport": {"width": 1728, "height": 1117}, "scale": 2, "mobile": False},
    "Windows Laptop HD": {"viewport": {"width": 1366, "height": 768}, "scale": 1, "mobile": False},

    # Desktop monitors
    "Desktop 1280×720": {"viewport": {"width": 1280, "height": 720}, "scale": 1, "mobile": False},
    "Desktop 1366×768": {"viewport": {"width": 1366, "height": 768}, "scale": 1, "mobile": False},
    "Desktop 1600×900": {"viewport": {"width": 1600, "height": 900}, "scale": 1, "mobile": False},
    "Desktop 1920×1080": {"viewport": {"width": 1920, "height": 1080}, "scale": 1, "mobile": False},
    "Desktop 2560×1440": {"viewport": {"width": 2560, "height": 1440}, "scale": 1, "mobile": False},
    "Desktop 3840×2160 (4K)": {"viewport": {"width": 3840, "height": 2160}, "scale": 1, "mobile": False},
}

# ✅ Prohlížeče
BROWSERS = ["chromium", "firefox", "webkit"]


@app.route("/")
def index():
    return render_template(
        "index.html",
        devices=list(DEVICE_PROFILES.keys()),
        aliases=URL_ALIASES,
        browsers=BROWSERS
    )


@app.route("/run_test", methods=["POST"])
def run_test():
    url = request.form.get("url")
    device = request.form.get("device")
    browser_name = request.form.get("browser")
    test_name = request.form.get("test_name", "test")

    profile = DEVICE_PROFILES.get(device)
    if not profile:
        return "❌ Neznámé zařízení"

    screenshot_name = f"{test_name}_{uuid.uuid4()}.png"
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)

    try:
        with sync_playwright() as p:
            browser = getattr(p, browser_name).launch(headless=True)
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)