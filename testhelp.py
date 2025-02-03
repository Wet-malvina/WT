import time
import random
from playwright.sync_api import Playwright, sync_playwright, expect

# Функция генерации случайного номера телефона
def generate_phone_number():
    operator_code = random.choice([901, 902, 903, 904, 905, 906, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 941, 950, 951, 953, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969])
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return '{} {}'.format(operator_code, number)

# Функция для выполнения теста
def run(playwright: Playwright, iteration: int) -> bool:
    # Запуск браузера с открытой панелью разработчика (DevTools)
    browser = playwright.chromium.launch(headless=False, devtools=True)
    context = browser.new_context()
    ##    record_har_path=f"har_logs/iteration_{iteration}.har"  # Запись сетевых запросов в файл HAR
    ##)
    page = context.new_page()

    try:
        page.goto("https://dev.parkuley.ru/parking/4d060434-511e-49c1-af91-7740fcff28d2?rentSmart")
        page.get_by_role("button", name="Открыть въезд").click()
        page.get_by_role("button", name="Завершить и оплатить").click()
        page.locator("input[name=\"phone\"]").fill(str(generate_phone_number()))
        page.get_by_role("button", name="Продолжить").click()
        page.get_by_placeholder("––––").fill("2211")
        page.wait_for_timeout(5000)
        page.get_by_label("Списать со счета (0").check()
        page.get_by_role("button", name="Оплатить").click()
        page.get_by_role("button", name="Открыть выезд").click()

        success = True
    except Exception as e:
        print(f"Ошибка: {e}")
        success = False
    finally:
        context.close()
        browser.close()

    return success

# Основной цикл
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
