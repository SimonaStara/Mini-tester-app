
import asyncio
from playwright.async_api import async_playwright

# ✅ Vestavěné profily Playwrightu (včetně Safari/WebKit zařízení)
BUILTIN_DEVICES = [
    "iPhone 12",
    "iPhone 13",
    "iPhone 14",
    "iPhone 14 Pro",
    "iPhone 15",
    "iPhone 15 Pro",
    "iPhone 15 Pro Max",
    "iPad Pro 11"
]

# ✅ Ručně definovaná nejnovější Samsung zařízení
SAMSUNG_DEVICES = {
    "Galaxy S22": {
        "viewport": {"width": 1080, "height": 2340},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent":
        "Mozilla/5.0 (Linux; Android 12; SM-S901B) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    },
    "Galaxy S23": {
        "viewport": {"width": 1080, "height": 2340},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent":
        "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    },
    "Galaxy S24": {
        "viewport": {"width": 1080, "height": 2340},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent":
        "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    }
}

async def run_test(url, browser_name="chromium", device_name="iPhone 15"):
    async with async_playwright() as p:

        browser_type = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit  # ✅ Safari/WebKit
        }.get(browser_name)

        if not browser_type:
            raise ValueError("❌ Neplatný prohlížeč (chromium/firefox/webkit)")

        browser = await browser_type.launch(headless=True)

        # ✅ Playwright built-in Apple zařízení (Safari i Chrome)
        if device_name in BUILTIN_DEVICES:
            profile = p.devices.get(device_name)
            context = await browser.new_context(**profile)

        # ✅ Samsung profily (ručně)
        elif device_name in SAMSUNG_DEVICES:
            context = await browser.new_context(**SAMSUNG_DEVICES[device_name])

        else:
            # ✅ fallback desktop
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0"
            )

        page = await context.new_page()

        print(f"🔎 Otevírám {url} jako {browser_name} + {device_name} ...")
        await page.goto(url)

        filename = f"screenshot_{browser_name}_{device_name.replace(' ', '_')}.png"
        await page.screenshot(path=filename)

        print(f"✅ Screenshot uložen jako: {filename}")

        await browser.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--browser", default="chromium",
                        choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--device",
                        default="iPhone 15",
                        choices=BUILTIN_DEVICES + list(SAMSUNG_DEVICES.keys()))
    args = parser.parse_args()

    asyncio.run(run_test(args.url, args.browser, args.device))
