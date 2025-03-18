import random
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="class")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


class TestUI:
    phone = f'+79321132{random.randint(100, 200)}'

    @pytest.mark.smoke
    def test_login(self, browser):
        link = "http://127.0.0.1:8000/"
        browser.get(link)
        form_number = browser.find_element(By.NAME, "phone_number")
        form_number.send_keys(self.phone)
        button = browser.find_element(By.NAME, "send")
        button.click()
        time.sleep(2)
        authentication_text = browser.find_element(By.TAG_NAME, "h3").text
        assert "enter the code sent to your phone number" == authentication_text

    @pytest.mark.smoke
    def test_auth(self, browser):
        link = "http://127.0.0.1:8000/authentication/"
        browser.get(link)
        cookie = browser.get_cookies()
        code = cookie[1]['value']
        form_code = browser.find_element(By.NAME, "authentication_code")
        form_code.send_keys(code)
        button = browser.find_element(By.NAME, "send_ok")
        button.click()
        time.sleep(2)
        account_text = browser.find_element(By.CLASS_NAME, "user").text
        assert f"User account: {self.phone}" == account_text

    @pytest.mark.smoke
    def test_account_add_invite(self, browser):
        link = "http://127.0.0.1:8000/account_access/"
        browser.get(link)
        form_invite_code = browser.find_element(By.ID, "invite_code")
        invite_code = "4@#94@"
        form_invite_code.send_keys(invite_code)
        button = browser.find_element(By.NAME, "add_code")
        button.click()
        time.sleep(2)
        account_text = browser.find_element(By.CLASS_NAME, "activate").text
        assert "Your code has been activated:" == account_text
