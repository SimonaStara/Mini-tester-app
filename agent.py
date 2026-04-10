from flask import Flask, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/run_test_local", methods=["POST"])
def run_test_local():
    data = request.json

    url = data.get("url")
    alias = data.get("alias")
    test_name = data.get("test_name", "test")
    device_name = data.get("device", "Desktop FullHD 1920×1080")

    # Informace pro log
    print("✅ Přijat požadavek z GUI:")
    print(f"URL: {url}")
    print(f"Alias: {alias}")
    print(f"Zařízení: {device_name}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)   # Otevře normální okno Chrome
            page = browser.new_page()

            # Jdeme na URL
            page.goto(url, timeout=60000)

            # Uděláme screenshot pro kontrolu
            screenshot_path = f"screenshot_{test_name}.png"
            page.screenshot(path=screenshot_path)

            title = page.title()

            browser.close()

        return f"""
        ✅ TEST PROBĚHL NA TVÉM NOTEBOOKU  
        🌍 URL: {url}  
        🪪 Název testu: {test_name}  
        🖼 Screenshot uložen jako: {screenshot_path}  
        🧾 Title stránky: {title}
        """

    except Exception as e:
        return f"❌ Test selhal: {str(e)}"


# ✅ Spustí lokální server dostupný i pro Railway
# (Railway posílá požadavek na tvoji IP:5001)
app.run(host="0.0.0.0", port=5001)