import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def test_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://dev.parkuley.ru/")
        page.wait_for_load_state("networkidle")
        try:
            page.get_by_role("button", name="Войти").click()
            page.locator("input[name=\"phone\"]").click()
            page.locator("input[name=\"phone\"]").fill("+7 920 363 75 68")
            page.get_by_role("button", name="Продолжить").click()
            page.get_by_placeholder("––––").fill("2211")
            page.get_by_role("link", name="Иваново, Лежневская улица, 128 ТЕСТ ЖК, 12 м").click()
            page.get_by_role("button", name="Транспортное средство й й й").click()
            page.get_by_role("button", name="Транспортное средство й й й").hover()
            time.sleep(1)
            page.get_by_role("button", name="й й й • й").page.locator(".lucide-icon.lucide.lucide-pencil").nth(2).click()
            page.get_by_role("button", name="Да", exact=True).click()

        except Exception as e:
            page.screenshot(path="screenshot_error.png")
            with open("page_source.html", "w", encoding="utf-8") as f:
                 f.write(page.content())
            print(f"Ошибка: {e}. Скриншот и HTML-код страницы сохранены.")
            raise
        finally:
            time.sleep(2)
            browser.close()
