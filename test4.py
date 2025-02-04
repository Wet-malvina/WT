import time
import json
import os
import random
from playwright.sync_api import sync_playwright, expect

def generate_phone_number():
    operator_code = random.choice([901, 902, 903, 904, 905, 906, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 941, 950, 951, 953, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969])
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return '{} {}'.format(operator_code, number)

phone_numbers = generate_phone_number()

DB_FILE = "users.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def test_interactions():
    users_db = load_db()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://dev.parkuley.ru")

        try:
            time.sleep(2)

            phone_number = random.choice(phone_numbers)
            print(f"Используемый номер телефона: {phone_number}")

            page.get_by_role("button", name="Войти").click()
            page.locator("input[name=\"phone\"]").fill(phone_numbers)
            page.get_by_role("button", name="Продолжить").click()
            page.get_by_placeholder("––––").fill("2211")



            time.sleep(2)
        except Exception as e:
            page.screenshot(path="screenshot_error.png")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"Ошибка: {e}. Скриншот и HTML-код страницы сохранены.")
            raise
        finally:
            time.sleep(2)
            browser.close()