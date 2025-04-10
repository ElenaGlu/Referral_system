import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from referral_app.models import UserProfile


@pytest.mark.smoke
@allure.title("Login with phone number")
def test_login(browser, stored_phone):
    link = "http://127.0.0.1:8000/"
    expected_text = "enter the code sent to your phone number"

    with allure.step("Открываем страницу логина"):
        browser.get(link)

    with allure.step(f"Вводим номер телефона: {stored_phone}"):
        phone_input = browser.find_element(By.NAME, "phone_number")
        phone_input.send_keys(stored_phone)

    with allure.step("Нажимаем кнопку отправки"):
        send_button = browser.find_element(By.NAME, "send")
        send_button.click()

    with allure.step("Ожидаем появления текста подтверждения"):
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), expected_text)
        )
    with allure.step("Проверяем, что отображается сообщение о вводе кода"):
        authentication_text = browser.find_element(By.TAG_NAME, "h3").text
        assert expected_text in authentication_text.lower()


def get_auth_code_from_db(stored_phone):
    try:
        auth_code = UserProfile.objects.filter(phone_number=stored_phone).order_by('-created_at').first()

        if auth_code:
            return auth_code.code
        else:
            raise Exception("Код для этого номера не найден")
    except Exception as e:
        print(f"Error: {e}")
        return None


@pytest.mark.smoke
@allure.title("Authentication using code from cookie")
def test_auth(browser, stored_phone):
    link = "http://127.0.0.1:8000/authentication/"

    with allure.step("Получаем код из базы по номеру"):
        code = get_auth_code_from_db(stored_phone)
        assert code is not None, "Код аутентификации не найден"

    with allure.step("Открываем страницу аутентификации"):
        browser.get(link)

    with allure.step("Ищем cookie с кодом аутентификации"):
        cookies = browser.get_cookies()
        code_cookie = next((c for c in cookies if c['name'] == 'a_code'), None)
        assert code_cookie is not None, "Кука a_code не найдена"
        code = code_cookie['value']

    with allure.step(f"Вводим код из cookie: {code}"):
        form_code = browser.find_element(By.NAME, "authentication_code")
        form_code.send_keys(code)

    with allure.step("Нажимаем кнопку подтверждения"):
        button = browser.find_element(By.NAME, "send_ok")
        button.click()

    with allure.step("Ожидаем отображение текста аккаунта"):
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user"))
        )
        account_text = browser.find_element(By.CLASS_NAME, "user").text

    with allure.step("Проверяем, что текст аккаунта соответствует ожидаемому"):
        assert f"User account: {stored_phone}" in account_text


@pytest.mark.smoke
@allure.title("Add invite code to account")
def test_account_add_invite(browser):
    link = "http://127.0.0.1:8000/account_access/"
    invite_code = "165187"
    expected_text = "Your code has been activated:"
    with allure.step("Открываем страницу добавления инвайт-кода"):
        browser.get(link)

    with allure.step(f"Вводим инвайт-код: {invite_code}"):
        form_invite_code = browser.find_element(By.ID, "invite_code")
        form_invite_code.send_keys(invite_code)

    with allure.step("Нажимаем кнопку 'Добавить код'"):
        button = browser.find_element(By.NAME, "add_code")
        button.click()

    with allure.step("Ожидаем появления текста об активации"):
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "activate"))
        )

    account_text = browser.find_element(By.CLASS_NAME, "activate").text
    assert expected_text in account_text.lower()
