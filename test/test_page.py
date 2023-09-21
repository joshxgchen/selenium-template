from selenium import webdriver
from selenium.webdriver.common.by import By
from e1utils import construct_headless_chrome_driver, get_landing_page_url, wait_for_page_load

def test_nonsecret_scenario():
    driver = construct_headless_chrome_driver()
    driver.get(get_landing_page_url())

    name_input = driver.find_element(By.ID, "preferredname")
    food_input = driver.find_element(By.ID, "food")
    password_input = driver.find_element(By.ID, "secret")  # Corrected the element ID

    name_input.send_keys("Josh")
    food_input.send_keys("Sushi")
    password_input.send_keys("password123")

    with wait_for_page_load(driver, 10):
        driver.find_element(By.ID, "submit").click()

    response_text = driver.find_element(By.XPATH, "/html/body").text
    assert "Thank you, Josh" in response_text
    assert "We also really like Sushi" in response_text

    # Assuming the button is not present in response.html
    secret_button = driver.find_elements(By.ID, "secretButton")
    assert len(secret_button) == 0

    driver.quit()

def test_secret_scenario():
    driver = construct_headless_chrome_driver()
    driver.get(get_landing_page_url())

    name_input = driver.find_element(By.ID, "preferredname")
    food_input = driver.find_element(By.ID, "food")
    password_input = driver.find_element(By.ID, "secret")  # Corrected the element ID

    name_input.send_keys("Josh")
    food_input.send_keys("Sushi")
    password_input.send_keys("magic")  # Updated to use the correct secret code

    with wait_for_page_load(driver, 10):
        driver.find_element(By.ID, "submit").click()

    response_text = driver.find_element(By.XPATH, "/html/body").text
    assert "Thank you, Josh" in response_text
    assert "We also really like Sushi" in response_text

    # Assuming the button is present in response.html
    with wait_for_page_load(driver, 10):
        driver.find_element(By.ID, "secretButton").click()

    assert "secret.html" in driver.current_url

    # Assuming this element is present in secret.html with the ID "secret_text"
    secret_text = driver.find_element(By.XPATH, "/html/body").text
    assert "Thanks for for being an extra special supporter, Josh." in secret_text
    assert "magic" in secret_text

    driver.quit()
