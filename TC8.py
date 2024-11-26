import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import requests as rq

# Test Data
homepage_url = "https://www.fitpeo.com"
#expected_reimbursement = "$11400"

# Set up WebDriver
try:
    # Set the path of the web browser
    Options = webdriver.ChromeOptions()
    Options.add_argument("--start-maximized")
    Options.add_argument("--headless")
    driver = webdriver.Chrome(options=Options)

    # Navigate to the FitPeo Homepage
    driver.get(homepage_url)

    # Verify the Homepage URL is loaded
    assert homepage_url in driver.current_url, "Error: The homepage URL did not load correctly."

    # Check the API Response
    api_response = rq.get(homepage_url)
    assert api_response.status_code == 200

    # Confirm page elements are accessible
    wait = WebDriverWait(driver, 10)
    logo_element = wait.until(ec.presence_of_element_located((By.XPATH, "//img[@alt='FitPeo']")))
    assert logo_element.is_displayed(), "Error: The FitPeo logo is not displayed on the homepage."

    print("Test Passed: The FitPeo homepage is accessible and functioning correctly.")

    # Click on the Revenue Calculator and navigate to the page
    revenue_page = driver.find_element(By.XPATH, "//div[text() = 'Revenue Calculator']")
    revenue_page.click()

    # Wait for the Revenue Calculator Page to load
    revenue_element = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='MuiBox-root css-rfiegf']/h4")))
    assert revenue_element.is_displayed(), "Error: The revenue page is not loaded"

    # Interact with the checkbox
    checkbox = driver.find_element(By.CSS_SELECTOR, "input.PrivateSwitchBase-input.css-1m9pwf3")
    checkbox.click()

    text_field = driver.find_element(By.CSS_SELECTOR, ".MuiInputBase-inputSizeSmall")

    text_field.clear()
    driver.execute_script("arguments[0].value = '200'; arguments[0].dispatchEvent(new Event('input'));", text_field)

    value_element = driver.find_element(By.XPATH, "//div[@class='MuiBox-root css-m1khva']/p[2]").text

    assert value_element == '$11400', "Total Recurring Reimbursement for all Patients Per Month is not matched"

except AssertionError as e:
    print(f"Test Failed: {e}")

except WebDriverException as e:
    print(f"WebDriver Error: {e}")

finally:
    # Close the Browser
    driver.quit()
