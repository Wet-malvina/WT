import time
import json
import os
import random
from playwright.sync_api import sync_playwright, expect

DB_FILE = "parkings.json"

PHONE_NUMBERS = [
    "+79201010400",
    "+79201010300",
    "+79201010100",
    "+79201010200"
]

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def test_interactions():
    parkings_db = load_db()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://dev.parkuley.ru")
        try:
                time.sleep(2)

                phone_number = random.choice(PHONE_NUMBERS)
                print(f"Используемый номер телефона: {phone_number}")

                page.get_by_role("button", name="Войти").click()
                page.locator("input[name=\"phone\"]").fill("+7 920 101 04 00")
                page.get_by_role("button", name="Продолжить").click()
                page.get_by_placeholder("––––").fill("1122")
                page.get_by_role("button", name="Сдать в аренду свою парковку").click()
                time.sleep(2)

                parking_name = "Парковка 1"
                address = "Иваново, Пророкова 31"
                vehicle_type = "Легковой"
                parking_type = "Открытая"
                price_per_hour = 1
                square = 11
                count_places = 11
                parking_url = page.url

                page.get_by_label("Название").click()
                page.get_by_label("Название").fill(parking_name)
                page.locator("input[name=\"address\"]").click()
                page.locator("input[name=\"address\"]").type("улица Пророкова, 31, Иваново", delay=100)
                time.sleep(2)
                page.get_by_role("button", name="Выберите тип ТС").click()
                page.get_by_role("button", name=vehicle_type).click()
                page.get_by_role("button", name="Выберите тип парковки").click()
                page.get_by_role("button", name=parking_type).click()
                page.get_by_text("Час").click()
                time.sleep(2)
                page.locator("input[name=\"priceHour\"]").click()
                page.locator("input[name=\"priceHour\"]").fill(str(price_per_hour))
                page.locator("input[name=\"square\"]").click()
                page.locator("input[name=\"square\"]").fill(str(square))
                page.locator("input[name=\"priceHour\"]").click()
                page.locator("input[name=\"priceHour\"]").fill(str(price_per_hour))
                page.locator("input[name=\"square\"]").click()
                page.locator("input[name=\"square\"]").fill(str(square))
                page.locator("input[name=\"countPlaces\"]").click()
                page.locator("input[name=\"countPlaces\"]").fill(str(count_places))
                page.get_by_label("Описание парковки").click()
                page.get_by_label("Описание парковки").fill("Лучшая парковка")

                parkings_db[parking_name] = {
                        "Ссылка": parking_url,
                        "Адрес": address,
                        "Тип ТС": vehicle_type,
                        "Тип парковки": parking_type,
                        "Количество мест": count_places,
                        "Тариф (руб/час)": price_per_hour
                }
                save_db(parkings_db)

                print(f"Данные о парковке '{parking_name}' сохранены в 'parkings.json'.")

                page.get_by_role("button", name="Вариант въезда и выезда").click()
                page.get_by_role("button", name="Лично").click()
                page.get_by_role("button", name="Добавить парковку").click()
                time.sleep(2)
                page.get_by_role("button", name="Клиент").click()
                page.get_by_role("button", name="Администратор").click()
                page.get_by_role("button", name="Поданные заявки").click()
                page.get_by_role("button", name="Опубликованные").click()
                page.get_by_role("button", name="Администратор").click()
                page.get_by_role("button", name="Клиент").click()
                page.get_by_role("button", name="Транспортное средство a a a").click()
                page.get_by_role("button", name="Добавить машину").click()
                time.sleep(2)
                page.locator("input[name=\"brand\"]").fill("й")
                page.locator("input[name=\"model\"]").click()
                page.locator("input[name=\"model\"]").fill("й")
                page.locator("input[name=\"number\"]").click()
                page.locator("input[name=\"number\"]").fill("й")
                page.locator("input[name=\"color\"]").click()
                page.locator("input[name=\"color\"]").fill("й")
                page.get_by_role("button", name="Тип ТС").click()
                page.get_by_role("button", name="Легковой", exact=True).click()
                page.get_by_role("button", name="Сохранить и выбрать").click()
                page.get_by_role("button", name="Забронировать").click()
                time.sleep(2)
                page.get_by_text("Списать со счета ").click()
                page.get_by_role("button", name="Оплатить").click()
                page.get_by_role("link", name="Парковка 1").click()
                page.get_by_role("button", name="Редактировать").click()
                page.get_by_role("button", name="Добавить тариф").click()
                page.get_by_role("button", name="Выберите тип ТС").click()
                page.get_by_role("button", name="Грузовой <7м").click()
                page.get_by_role("button", name="Выберите тип парковки").click()
                page.get_by_role("button", name="Открытая").nth(1).click()
                time.sleep(2)
                page.locator(
                 "div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div > .grid > label > .w-6").first.click()
                page.locator("input[name=\"priceHour\"]").nth(1).click()
                page.locator("input[name=\"priceHour\"]").nth(1).fill("1")
                page.locator("input[name=\"square\"]").nth(1).click()
                page.locator("input[name=\"square\"]").nth(1).fill("11")
                page.locator("input[name=\"countPlaces\"]").nth(1).click()
                page.locator("input[name=\"countPlaces\"]").nth(1).fill("11")
                page.get_by_role("button", name="Обновить парковку").click()
                page.get_by_role("button", name="Транспортное средство й й й").click()
                page.get_by_role("button", name="а а а • а").hover()
                page.get_by_role("button", name="й й й • й").hover()
                page.get_by_role("button", name="й й й • й").get_by_role("button").nth(1).click()
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
