import os
import datetime
import requests
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
SCREENSHOT_DIR = "static/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# URL aliasy
URL_ALIASES = {
    "Seznam – homepage": "https://seznam.cz",
    "Google": "https://google.com",
    "IDNES": "https://idnes.cz",
    "Mall – produkce": "https://mall.cz"
}

# Zařízení
DEVICE_PROFILES = {
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

    "iPad Mini": {"viewport": {"width": 768, "height": 1024}, "scale": 2, "mobile": True},
    "iPad Air": {"viewport": {"width": 820, "height": 1180}, "scale": 2, "mobile": True},
    "iPad Pro 11": {"viewport": {"width": 834, "height": 1194}, "scale": 2, "mobile": True},
    "iPad Pro 12.9": {"viewport": {"width": 1024, "height": 1366}, "scale": 2, "mobile": True},

    "Samsung S21": {"viewport": {"width": 1080, "height": 2400}, "scale": 3, "mobile": True},
    "Samsung S21 Ultra": {"viewport": {"width": 1440, "height": 3200}, "scale": 3, "mobile": True},
    "Samsung S22": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S22 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung S23": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S23 Ultra": {"viewport": {"width": 1440, "height": 3088}, "scale": 3, "mobile": True},
    "Samsung S24": {"viewport": {"width": 1080, "height": 2340}, "scale": 3, "mobile": True},
    "Samsung S24 Ultra": {"viewport": {"width": 1440, "height": 3120}, "scale": 3, "mobile": True},
}

@app.route("/")
def index():
    return render_template(
        "index.html",
        devices=list(DEVICE_PROFILES.keys()),
        aliases=URL_ALIASES
    )

# ✅ NOVÁ VERZE /run_test → přeposílá test na tvůj notebook
@app.route("/run_test", methods=["POST"])
def run_test():

    data = request.form.to_dict()

    # ✅ DOSAĎ TVŮJ IP A PORT
    LOCAL_AGENT_URL = "https://repeated-slashed-dynasty.ngrok-free.dev/run_test_local"

    try:
        r = requests.post(LOCAL_AGENT_URL, json=data, timeout=20)
        return r.text
    except Exception as e:
        return f"❌ Lokální agent neodpovídá – je spuštěný? ({e})"

if __name__ == "__main__":
    app.run(debug=True)