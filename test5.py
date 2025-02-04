import time
import json
import os
import random
from playwright.sync_api import sync_playwright, expect
from playwright.sync_api import Playwright


def run(playwright: Playwright, iteration: int) -> bool:
    browser = playwright.chromium.launch(headless=False, devtools=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("https://dev.parkuley.ru/parking/894b9a5d-a6fa-47b8-b0a3-42b4c585108d?rentSmart")
        page.get_by_role("button", name="Открыть въезд").click()

        success = True
    except Exception as e:
        print(f"Ошибка: {e}")
        success = False
    finally:
        context.close()
        browser.close()

    return success


def main():
    max_iterations = 100
    successful_iterations = 0

    with sync_playwright() as playwright:
        for i in range(1, max_iterations + 1):
            print(f"Запуск теста {i}...")
            if run(playwright, i):
                successful_iterations += 1
            else:
                print(f"Тест {i} завершился с ошибкой. Останавливаем тестирование.")
                break

    print(f"Всего успешных итераций: {successful_iterations}")

if __name__ == "__main__":
    main()
