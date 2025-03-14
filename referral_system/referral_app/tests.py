import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


link = "http://127.0.0.1:8000/"
try:
    browser = webdriver.Chrome()
    browser.get(link)
    button_number = browser.find_element(By.NAME, "phone_number")
    button_number.send_keys("+79321132149")

    button = browser.find_element(By.NAME, "send")
    button.click()
    time.sleep(1)
    authentication = browser.find_element(By.TAG_NAME, "h3")
    authentication_text = authentication.text
    cookie = browser.get_cookies()
    code = cookie[1]['value']
    button_code = browser.find_element(By.NAME, "authentication_code")
    button_code.send_keys(code)
    button = browser.find_element(By.NAME, "send_ok")

    assert "enter the code sent to your phone number" == authentication_text

finally:
    time.sleep(3)
    browser.quit()
