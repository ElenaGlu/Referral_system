from urllib.parse import urlparse

from conftest import get_auth_code_from_db, get_invite_code_from_db

import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.django_db()


@pytest.mark.smoke
@allure.title("Login with phone number")
def test_login(live_server, browser, stored_phone, postgres_test_db):
    link = f"{live_server.url}/"
    expected_text = "enter the code sent to your phone number"

    PHONE_INPUT = (By.NAME, "phone_number")
    SEND_BUTTON = (By.NAME, "send")
    HEADER = (By.TAG_NAME, "h3")

    with allure.step("Открываем страницу логина"):
        browser.get(link)

    with allure.step(f"Вводим номер телефона: {stored_phone}"):
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(PHONE_INPUT)
        ).send_keys(stored_phone)

    with allure.step("Нажимаем кнопку отправки"):
        browser.find_element(*SEND_BUTTON).click()

    with allure.step("Ожидаем отображение заголовка подтверждения"):
        header = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(HEADER)
        )
        assert expected_text in header.text.lower()


@pytest.mark.smoke
@allure.title("Authentication using code from cookie")
def test_auth(live_server, browser, postgres_test_db):
    AUTH_PAGE = f"{live_server.url}/authentication/"
    CODE_INPUT = (By.NAME, "authentication_code")
    SUBMIT_BUTTON = (By.NAME, "send_ok")
    USER_TEXT = (By.CLASS_NAME, "user")

    with allure.step("Получаем код из базы по номеру"):
        code, access_token, phone_number = get_auth_code_from_db()
        assert code is not None, "Код аутентификации не найден"

    with allure.step("Заходим на домен для установки куки"):
        browser.get(live_server.url)
        domain = urlparse(live_server.url).hostname

    with allure.step("Добавляем access_token в cookie"):
        browser.add_cookie({
            "name": "jwt",
            "value": access_token,
            "path": "/",
            "domain": domain
        })

    with allure.step("Переходим на страницу аутентификации"):
        browser.get(AUTH_PAGE)

    with allure.step(f"Вводим код из cookie: {code}"):
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(CODE_INPUT)
        ).send_keys(code)

    with allure.step("Нажимаем кнопку подтверждения"):
        browser.find_element(*SUBMIT_BUTTON).click()

    with allure.step("Ожидаем отображение текста аккаунта"):
        user_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(USER_TEXT)
        )

    with allure.step("Проверяем, что текст аккаунта соответствует ожидаемому"):
        assert f"User account: {phone_number}" in user_element.text


@pytest.mark.smoke
@allure.title("Add invite code to account")
def test_account_add_invite(live_server, browser, postgres_test_db):
    INVITE_PAGE = f"{live_server.url}/account_access/"
    INVITE_INPUT = (By.ID, "invite_code")
    ADD_BUTTON = (By.NAME, "add_code")
    RESULT_TEXT = (By.CLASS_NAME, "activate")
    EXPECTED_TEXT = "your code has been activated:"

    with allure.step("Получаем access_token и инвайт-код из БД"):
        access_token, invite_code = get_invite_code_from_db()
        assert access_token and invite_code, "Не удалось получить данные из БД"

    with allure.step("Заходим на домен, чтобы установить куку"):
        browser.get(live_server.url)
        domain = urlparse(live_server.url).hostname

    with allure.step("Устанавливаем JWT токен в cookie"):
        browser.add_cookie({
            "name": "jwt",
            "value": access_token,
            "path": "/",
            "domain": domain
        })

    with allure.step("Открываем страницу добавления инвайт-кода"):
        browser.get(INVITE_PAGE)

    with allure.step(f"Вводим инвайт-код: {invite_code}"):
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(INVITE_INPUT)
        ).send_keys(invite_code)

    with allure.step("Нажимаем кнопку 'Добавить код'"):
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(ADD_BUTTON)
        ).click()

    with allure.step("Ожидаем появления текста об активации"):
        result_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(RESULT_TEXT)
        )

    with allure.step("Проверяем, что код активирован"):
        actual_text = result_element.text.lower()
        assert EXPECTED_TEXT in actual_text, (
            f"Ожидали текст '{EXPECTED_TEXT}', но получили: '{actual_text}'"
        )
