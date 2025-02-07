import time
from playwright.sync_api import sync_playwright, expect
from playwright.sync_api import Playwright

def test_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://dev.parkuley.ru/parking/05760dba-e90b-4bee-a9d3-ce0938a3b160")

        try:
            print("Открытие страницы и вход")
            page.get_by_role("button", name="Войти").click()
            page.locator("input[name=\"phone\"]").fill("+7 920 363 75 68")
            page.get_by_role("button", name="Продолжить").click()
            page.get_by_placeholder("––––").fill("2211")
            time_exit = page.locator(
                ".relative popover-container flex flex-1 w-full svelte-1fhy0ll").nth(1).inner_text().strip()
            print(f"Время выезда при бронировании: {time_exit}")

            page.get_by_role("button", name="Забронировать").click()

            page.get_by_label("Списать со счета").check()
            page.get_by_role("button", name="Оплатить").click()

            page.get_by_role("button", name="Заказ №").click()

            time_exit_order = page.locator(
                "flex w-full flex-col px-3 py-1 border border-neutral-500 border-l-0 rounded-lg rounded-l-none rounded-b-none").nth(0).inner_text().strip()
            print(f"Время выезда в заказе: {time_exit_order}")
            if time_exit != time_exit_order:
                raise AssertionError(f"Ошибка: время выезда не совпадает! "
                                     f"Ожидалось: {time_exit}, а в заказе: {time_exit_order}")
            else:
                print("Время выезда совпадает!")

        except Exception as e:
            page.screenshot(path="screenshot_error.png")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"Ошибка: {e}. Скриншот и HTML-код страницы сохранены.")
            raise

        finally:
            time.sleep(2)
            browser.close()



