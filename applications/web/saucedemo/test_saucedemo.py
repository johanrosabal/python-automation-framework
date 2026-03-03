import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Fixture to initialize and quit the WebDriver
@pytest.fixture
def driver():
    # Initialize WebDriver (ensure chromedriver is in your PATH)
    driver = webdriver.Chrome()
    # Implicit wait: Pauses the script until the element is loaded.
    driver.implicitly_wait(10)  # Wait 10 seconds
    driver.maximize_window()

    yield driver
    # Quit the browser after the test
    driver.quit()


# Test to verify successful login on Sauce Demo
def test_login(driver):

    # Navigate to the login page
    driver.get("https://www.saucedemo.com/v1/index.html")

    # Find the username field and enter username
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")


    # Find the password field and enter password
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")

    # Click the login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # Wait some seconds
    # time.sleep(5)

    # Verify that the URL contains "inventory" to confirm a successful login
    assert "inventory" in driver.current_url, "Login failed"



