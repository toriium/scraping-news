from selenium import webdriver
from selenium_toolkit import SeleniumToolKit


def get_selenium_webdriver() -> SeleniumToolKit:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    stk = SeleniumToolKit(driver)
    return stk
