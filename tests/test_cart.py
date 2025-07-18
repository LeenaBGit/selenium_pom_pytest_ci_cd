import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (for CI)
    options.add_argument('--no-sandbox')  # Required for some CI environments
    options.add_argument('--disable-dev-shm-usage')  # Avoid memory issues

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_single_item(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()
    assert inventory.get_cart_count() == "1"

def test_add_two_items(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()
    time.sleep(1)
    inventory.add_bike_light_to_cart()
    time.sleep(1)
    assert inventory.get_cart_count() == "2"
