import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def google_search(query, debug=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--blink-settings=imagesEnabled=false")  # Skip images
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--dns-prefetch-disable")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    # Block images, fonts, media via CDP for faster page loads
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*.png", "*.jpg", "*.gif", "*.svg", "*.woff", "*.woff2", "*.mp4", "*.css"]
    })
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )

    try:
        t0 = time.time()

        driver.get("https://www.google.com")

        # Dismiss consent popup (fast, short timeout)
        for xpath in [
            '//button[.//span[contains(text(),"Accept all")]]',
            '//button[contains(text(),"Accept all")]',
            '//button[contains(text(),"I agree")]',
        ]:
            try:
                btn = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                break
            except Exception:
                pass

        # Type query all at once (no per-char delay)
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query + Keys.RETURN)

        # Wait only for what we need
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        if debug:
            print(driver.page_source[:3000])

        # Extract results
        results = []
        search_div = driver.find_element(By.ID, "search")

        for h3 in search_div.find_elements(By.CSS_SELECTOR, "h3"):
            try:
                title = h3.text.strip()
                if not title:
                    continue

                link = ""
                try:
                    link = h3.find_element(By.XPATH, "ancestor::a[1]").get_attribute("href") or ""
                except Exception:
                    pass

                snippet = ""
                try:
                    container = h3.find_element(By.XPATH, "ancestor::div[contains(@class,'g')][1]")
                    for sel in [".VwiC3b", "[data-sncf='1']", ".lEBKkf"]:
                        try:
                            snippet = container.find_element(By.CSS_SELECTOR, sel).text.strip()
                            if snippet:
                                break
                        except Exception:
                            pass
                except Exception:
                    pass

                if title and link.startswith("http") and "google.com" not in link:
                    results.append((title, link, snippet))
                    if len(results) == 10:
                        break

            except Exception:
                continue

        print(f"\n🔍 Results for: '{query}'  ({time.time() - t0:.1f}s)")
        print("=" * 60)
        for i, (title, link, snippet) in enumerate(results, 1):
            print(f"\n{i}. {title}")
            print(f"   {link}")
            if snippet:
                print(f"   {snippet[:150]}{'...' if len(snippet) > 150 else ''}")

        return results    

    finally:
        driver.quit()
"""

if __name__ == "__main__":
    url='intitle:"index of" inurl:backup'
    google_search(url)

"""
