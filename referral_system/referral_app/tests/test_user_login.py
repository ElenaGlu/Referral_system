from django.urls import reverse

import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.django_db()


@pytest.mark.regression
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


@pytest.mark.django_db
@pytest.mark.parametrize('payload', [
    {'phone_number': '9991234567'},
    {'phone_number': '+7999ABC@567'},
    {'phone_number': '+799912345678901000'},
    {'phone_number': '+44999123567'},
    {'phone': '+79321132149'},
    {'phone_number': ''},
    {},
])
def test_user_login_invalid_phone_number(client, payload):
    response = client.post(reverse('user_login'), data=payload, format='json')
    assert response.status_code == 302
    assert response.url == reverse('user_login')
