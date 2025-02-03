import time
from playwright.sync_api import sync_playwright, expect

def test_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://dev.parkuley.ru/parking/7d76cd37-6c5d-415f-9326-a7f8d6905f9b")
        try:
            print("Открытие страницы и вход")
            page.get_by_role("button", name="Войти").click()

            print("Ввод номера телефона")
            page.locator("input[name='phone']").fill("9201010100")

            print("Нажатие кнопки 'Продолжить'")
            page.get_by_role("button", name="Продолжить").click()

            print("Ввод кода подтверждения")
            page.get_by_placeholder("––––").fill("1122")
            time.sleep(1)

            print("Нажатие кнопки 'Забронировать'")
            page.get_by_role("button", name="Забронировать").click()

            print("Выбор списать со счета")
            page.get_by_label("Списать со счета ").check()

            print("Нажатие кнопки 'Оплатить'")
            page.get_by_role("button", name="Оплатить").click()

            print("Проверка наличия текста")
            expect(page.get_by_text("Спасибо, оплата прошла!")).to_be_visible()

            page.screenshot(path=f"screenshot_success.png")
            print("Тест успешно выполнен. Скриншот сохранен.")
        except Exception as e:
            page.screenshot(path=f"screeshot_error.png")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())
                print (f"Ошибка: {e}. Скриншот и HTML-код страницы сохранены.")
                raise
        finally:
            time.sleep(2)
            browser.close()