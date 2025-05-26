from django.urls import reverse
from urllib.parse import urlparse

from conftest import get_auth_code_from_db

import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


pytestmark = pytest.mark.django_db()


@pytest.mark.regression
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


@pytest.mark.django_db
@pytest.mark.parametrize('payload', [
    {'authentication_code': '51139!'},
    {'authentication_code': '11'},
    {'authentication_code': '12345'},
    {'authentication_code': '1@a8'},
    {'authentication': '1234'},
    {'authentication_code': ''},
    {},
])
def test_user_authentication_invalid_code(client, payload):
    # client.cookies['jwt'] = 'fake.jwt.token'
    response = client.post(reverse('user_authentication'), data=payload, format='json')
    assert response.status_code == 302
    assert response.url == reverse('user_authentication')
