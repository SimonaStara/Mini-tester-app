import os
import datetime
from flask import Flask, render_template, request, send_from_directory
from playwright.sync_api import sync_playwright

app = Flask(__name__)
SCREENSHOT_DIR = "static/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# URL aliasy — můžeš libovolně rozšířit
URL_ALIASES = {
    "Seznam – homepage": "https://seznam.cz",
    "Google": "https://google.com",
    "IDNES": "https://idnes.cz",
    "Mall – produkce": "https://mall.cz"
}

# ✅ MEGA SEZNAM ZAŘÍZENÍ – pro interaktivní emulaci přes Chromium
DEVICE_PROFILES = {

    # 📱 iPhone – kompletní sada
    "iPhone SE": {"viewport": {"width": 375, "height": 667}, "scale": 2, "mobile": True},
    "iPhone XR": {"viewport": {"width": 414, "height": 896}, "scale": 2, "mobile": True},
    "iPhone 11": {"viewport": {"width": 414, "height": 896}, "scale": 2, "mobile": True},
    "iPhone 12": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPhone 12 Pro Max": {"viewport": {"width": 428, "height": 926}, "scale": 3, "mobile": True},
    "iPhone 13": {"viewport": {"width": 390, "height": 844}, "scale": 3, "mobile": True},
    "iPhone 13 Pro Max": {"viewport": {"width": 428, "height": 926}, "scale": 3, "mobile": True},
    "iPhone 14": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 14 Pro Max": {"viewport": {"width": 430, "height": 932}, "scale": 3, "mobile": True},
    "iPhone 15": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 15 Plus": {"viewport": {"width": 430, "height": 932}, "scale": 3, "mobile": True},
    "iPhone 15 Pro": {"viewport": {"width": 393, "height": 852}, "scale": 3, "mobile": True},
    "iPhone 15 Pro Max": {"viewport": {"width": 430, "height": 932}, "scale": 3, "mobile": True},

    # 📱 iPad – kompletní sada
    "iPad Mini": {"viewport": {"width": 768, "height": 1024}, "scale": 2, "mobile": True},
    "iPad Air": {"viewport": {"width": 820, "height": 1180}, "scale": 2, "mobile": True},
    "iPad Pro 11": {"viewport": {"width": 834, "height": 1194}, "scale": 2, "mobile": True},
    "iPad Pro 12.9": {"viewport": {"width": 1024, "height": 1366}, "scale": 2, "mobile": True},

    # 🤖 Samsung
    "Samsung S21": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Samsung S21 Ultra": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Samsung S22": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S22 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung S23": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S23 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung S24": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S24 Ultra": {"viewport": {"width": 1440, "height": 3120}, "scale": 3, "mobile": True},
    "Galaxy Z Flip": {"viewport": {"width": 1080, "height": 2640}, "scale": 3, "mobile": True},
    "Galaxy Z Fold": {"viewport": {"width": 1536, "height": 2152}, "scale": 3, "mobile": True},

    # 🤖 Xiaomi / Huawei / Pixel
    "Xiaomi 13 Pro": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Huawei P60": {"viewport": {"width": 1220, "height": 2700}, "scale": 3, "mobile": True},
    "Google Pixel 7": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Google Pixel 8 Pro": {"viewport": {"width": 1344, "height": 2992}, "scale": 3, "mobile": True},

    # 💻 MacBook / Desktop
    "MacBook Air 13": {"viewport": {"width": 1440, "height": 900}, "scale": 2, "mobile": False},
    "MacBook Pro 14": {"viewport": {"width": 1512, "height": 982}, "scale": 2, "mobile": False},
    "MacBook Pro 16": {"viewport": {"width": 1728, "height": 1117}, "scale": 2, "mobile": False},

    # 🖥️ Desktop monitory
    "Desktop HD 1366×768": {"viewport": {"width": 1366, "height": 768}, "scale": 1, "mobile": False},
    "Desktop FullHD 1920×1080": {"viewport": {"width": 1920, "height": 1080}, "scale": 1, "mobile": False},
    "Desktop 2K 2560×1440": {"viewport": {"width": 2560, "height": 1440}, "scale": 1, "mobile": False},
    "Desktop 4K 3840×2160": {"viewport": {"width": 3840, "height": 2160}, "scale": 1, "mobile": False},
    "Ultrawide 3440×1440": {"viewport": {"width": 3440, "height": 1440}, "scale": 1, "mobile": False}
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        devices=list(DEVICE_PROFILES.keys()),
        aliases=URL_ALIASES
    )


@app.route("/run_test", methods=["POST"])
def run_test():

    alias = request.form["alias"]
    url_manual = request.form["url"]
    test_name = request.form["test_name"].strip()
    device_name = request.form["device"]

    url = URL_ALIASES[alias] if alias != "none" else url_manual
    if test_name == "":
        test_name = "test"

    profile = DEVICE_PROFILES[device_name]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            viewport=profile["viewport"],
            is_mobile=profile["mobile"],
            has_touch=True,
            device_scale_factor=profile["scale"],
            user_agent="Mozilla/5.0",      # univerzální UA → přepsán popř. ručně
            ignore_https_errors=True
        )

        page = context.new_page()

        # ✅ popup fix → žádné about:blank!
        page.add_init_script("""
            window.open = function(url) {
                window.location.href = url;
            };
        """)

        page.goto(url)

        input("\n👉 Po dokončení práce v okně Chrome stiskni ENTER pro screenshot...\n")

        today = datetime.date.today().strftime("%Y-%m-%d")
        folder = os.path.join(SCREENSHOT_DIR, today)
        os.makedirs(folder, exist_ok=True)

        file = f"{test_name}_{device_name.replace(' ','_')}.png"
        path = os.path.join(folder, file)

        page.screenshot(path=path)

        browser.close()

        return send_from_directory(folder, file)


if __name__ == "__main__":
    app.run(debug=True)



