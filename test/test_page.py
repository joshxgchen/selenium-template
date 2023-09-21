from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from e1utils import construct_headless_chrome_driver, get_landing_page_url, wait_for_page_load


def test_nonsecret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    try:
        # Open the landing page
        driver.get(landing_page)

        # Find and interact with form elements
        name_input = driver.find_element(By.ID, "preferredname")
        food_input = driver.find_element(By.ID, "food")
        secret_input = driver.find_element(By.ID, "secret")
        submit_button = driver.find_element(By.ID, "submit")

        # Fill in form fields
        name_input.send_keys("John Doe")
        food_input.send_keys("Pizza")
        secret_input.send_keys("mysecretcode")

        # Submit the form
        submit_button.click()

        # Wait for the response page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://yourwebsite.com/response.html"))

        # Assert expected content on the response page
        assert "Thank you, John Doe," in driver.page_source
        assert "We also really like Pizza," in driver.page_source

        # Assert that the button is not present on the page
        assert len(driver.find_elements(By.ID, "secretButton")) == 0

    finally:
        driver.quit()


def test_secret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    try:
        # Open the landing page
        driver.get(landing_page)

        # Find and interact with form elements
        name_input = driver.find_element(By.ID, "preferredname")
        food_input = driver.find_element(By.ID, "food")
        secret_input = driver.find_element(By.ID, "secret")
        submit_button = driver.find_element(By.ID, "submit")

        # Fill in form fields
        name_input.send_keys("Jane Smith")
        food_input.send_keys("Sushi")
        secret_input.send_keys("magic")

        # Submit the form
        submit_button.click()

        # Wait for the response page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://yourwebsite.com/response.html"))

        # Assert expected content on the response page
        assert "Thank you, Jane Smith," in driver.page_source
        assert "We also really like Sushi," in driver.page_source

        # Check for the "Take me to the secrets" button
        assert "Take me to the secrets." in driver.page_source

        # Click the "Take me to the secrets" button
        secret_button = driver.find_element(By.ID, "secretButton")
        secret_button.click()

        # Wait for the secret page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://yourwebsite.com/secret.html"))

        # Assert expected content on the secret page
        assert "Thanks for being an extra special supporter, Jane Smith." in driver.page_source
        assert "We know that you find our company has a little extra magic." in driver.page_source

    finally:
        driver.quit()


