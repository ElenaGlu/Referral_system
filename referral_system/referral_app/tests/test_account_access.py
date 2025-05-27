from django.urls import reverse
from urllib.parse import urlparse

from conftest import get_invite_code_from_db, get_auth_code_from_db

import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.django_db()


@pytest.mark.regression
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


@pytest.mark.django_db
def test_account_access_without_authentication(client):
    response = client.get(reverse('account_access'))
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize('payload', [
    {'invite_code': '12&'},
    {'invite_code': '1234567890000'},
    {'invite': '123456'},
    {'invite_code': ''},
    {},
])
def test_invalid_invite_code(client, payload, postgres_test_db):
    code, access_token, phone_number = get_auth_code_from_db()
    client.cookies['jwt'] = access_token
    response = client.post(reverse('account_access'), data=payload)
    assert response.status_code == 302
    assert response.url == reverse('account_access')
