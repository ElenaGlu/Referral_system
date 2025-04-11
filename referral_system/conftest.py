import random

import pytest
from loguru import logger
from selenium import webdriver

from referral_app import models
from referral_app.models import UserProfile


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("browser_name")
    browser = None
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        browser = webdriver.Chrome()
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        geckodriver_path = "/snap/bin/geckodriver"
        driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
        browser = webdriver.Firefox(service=driver_service)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()


@pytest.fixture()
def stored_phone():
    while True:
        operator_code = random.randint(900, 999)
        subscriber_number = random.randint(1000000, 9999999)
        phone_number = f"+7{operator_code}{subscriber_number:07d}"
        return phone_number


@pytest.fixture()
def postgres_test_db():
    user = [
        {
            "id": 2,
            "phone_number": "+79321132155",
            "authentication_code": "0467",
            "invite_code": "8113@6",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NDMwMDIzOX0.iYaY3M7LP71WdcOVa591r3DginEIbk9NjZ_jv0nmVcU",
            "used_code": "652@91",
        },

    ]
    temporary = []
    for obj in user:
        temporary.append(models.UserProfile(**obj))

        models.UserProfile.objects.bulk_create(temporary)
        logger.info(UserProfile.objects.all().values())
        return None

 # temp = [models.UserProfile(**obj) for obj in user]