import asyncio
import random
import time
from playwright.async_api import async_playwright

TOTAL_USERS = 5
EXIT_USERS = 2

USER_CREDENTIALS = [
    {"phone": "+79201010612", "first_name": "Анна", "last_name": "Иванова", "email": "anna.ivanova@gmail.com"},
    {"phone": "+79201010002", "first_name": "Мария", "last_name": "Петрова", "email": "maria.petrova@yandex.ru"},
    {"phone": "+79201010003", "first_name": "Екатерина", "last_name": "Сидорова", "email": "ekaterina.sidorova@mail.ru"},
    {"phone": "+79201010004", "first_name": "Ольга", "last_name": "Кузнецова", "email": "olga.kuznetsova@rambler.ru"},
    {"phone": "+79201010015", "first_name": "Татьяна", "last_name": "Попова", "email": "tatiana.popova@outlook.com"},]
    #{"phone": "+79201010006", "first_name": "Наталья", "last_name": "Смирнова", "email": "natalia.smirnova@gmail.com"},
    #{"phone": "+79201010007", "first_name": "Елена", "last_name": "Васильева", "email": "elena.vasileva@yandex.ru"},
    #{"phone": "+79201010008", "first_name": "Светлана", "last_name": "Федорова", "email": "svetlana.fedorova@mail.ru"},
    #{"phone": "+79201010009", "first_name": "Алина", "last_name": "Морозова", "email": "alina.morozova@rambler.ru"},
    #{"phone": "+79201010010", "first_name": "Дарья", "last_name": "Новикова", "email": "daria.novikova@outlook.com"},
    #{"phone": "+79201010011", "first_name": "Вероника", "last_name": "Зайцева", "email": "veronika.zaytseva@gmail.com"},
    #{"phone": "+79201010012", "first_name": "Анастасия", "last_name": "Соловьева", "email": "anastasia.solovieva@yandex.ru"},
    #{"phone": "+79201010013", "first_name": "Виктория", "last_name": "Михайлова", "email": "victoria.mikhailova@mail.ru"},
    #{"phone": "+79201010014", "first_name": "Кристина", "last_name": "Беляева", "email": "kristina.belyaeva@rambler.ru"},
    #{"phone": "+79201010015", "first_name": "Полина", "last_name": "Тихонова", "email": "polina.tikhonova@outlook.com"},
#]


async def user_actions(context, user, user_index):
    page = await context.new_page()
    await page.goto("https://dev.parkuley.ru")
    await page.wait_for_load_state("networkidle")

    print(f"👤 [User {user_index}] Авторизация {user['phone']}")

    await page.get_by_role("button", name="Войти").click()
    await page.locator("input[name='phone']").fill(user["phone"])
    await page.get_by_role("button", name="Продолжить").click()
    await page.get_by_placeholder("––––").fill("2211")
    await page.locator("input[name=\"name\"]").click()
    await page.locator("input[name=\"name\"]").fill(user["first_name"])
    await page.locator("input[name=\"surname\"]").click()
    await page.locator("input[name=\"surname\"]").fill(user["last_name"])
    await page.locator("input[name=\"email\"]").click()
    await page.get_by_role("button", name="Зарегистрироваться").click()

    await page.wait_for_timeout(2000)

    print(f" [User {user_index}] Авторизовался!")

    start_time = time.time()
    try:
        while time.time() - start_time < 300:
            await page.wait_for_timeout(random.randint(1000, 3000))  # Случайные задержки между действиями

            action = random.choice(["Просмотр парковок", "Создание парковки", "Бронирование"])
            if action == "Просмотр парковок":
                await page.get_by_role("link", name="Иваново, Лежневская улица, 128 ТЕСТ ЖК, 12 м").click()
            elif action == "Создание парковки":
                await page.get_by_role("button", name="Сдать в аренду свою парковку").click()
                time.sleep(4)
                await page.get_by_role("button", name="Отмена").click()
            elif action == "Бронирование":
                await page.get_by_role("link", name="Иваново, улица Пророкова, 8 3").click()
                await page.get_by_role("button", name="Назад").click()


            print(f" [User {user_index}] Совершил действие: {action}")


            if user_index < EXIT_USERS and time.time() - start_time > 180:
                print(f" [User {user_index}] Вышел из системы!")
                await page.get_by_role("button", name="Выйти").click()
                break
    except Exception as e:
        print(f" Ошибка у {user['phone']}: {e}")
        await page.screenshot(path=f"error_{user_index}.png")
    finally:
        await context.close()


async def run_all_users():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = []


        for i, user in enumerate(USER_CREDENTIALS):
            context = await browser.new_context()
            task = asyncio.create_task(user_actions(context, user, i))
            tasks.append(task)

        await asyncio.gather(*tasks)

        await browser.close()


asyncio.run(run_all_users())
