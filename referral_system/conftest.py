import random
import pytest
from selenium import webdriver

from referral_app import models
from referral_app.models import UserProfile


@pytest.fixture
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


@pytest.fixture
def stored_phone():
    while True:
        operator_code = random.randint(900, 999)
        subscriber_number = random.randint(1000000, 9999999)
        phone_number = f"+7{operator_code}{subscriber_number:07d}"
        return phone_number


@pytest.fixture
def postgres_test_db():
    user = [
        {
            "id": 2,
            "phone_number": "+79321132155",
            "authentication_code": "0467",
            "invite_code": "8113@6",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "used_code": "652@91",
        },
        {
            "id": 3,
            "phone_number": "+79321132144",
            "authentication_code": "8333",
            "invite_code": "51139!",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCH5",
            "used_code": None,
        },

    ]
    temp = [models.UserProfile(**obj) for obj in user]
    return models.UserProfile.objects.bulk_create(temp)


def get_auth_code_from_db():
    try:
        user = UserProfile.objects.get(phone_number="+79321132155")
        if user:
            return user.authentication_code, user.access_token, user.phone_number
        else:
            raise Exception("Код для этого номера не найден")
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_invite_code_from_db():
    try:
        user = UserProfile.objects.get(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCH5")
        if user:
            user_invite = UserProfile.objects.get(invite_code="8113@6")
            return user.access_token, user_invite.invite_code
        else:
            raise Exception("Инвайт-кода не существует")
    except Exception as e:
        print(f"Error: {e}")
        return None


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
