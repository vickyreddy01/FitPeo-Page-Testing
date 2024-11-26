import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import requests as rq

# Test Data
homepage_url = "https://www.fitpeo.com"

#Set up WebDriver
try:
    # Set the path of the web browser
    Options = webdriver.ChromeOptions()
    Options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=Options)

    # Navigate to the FitPeo Homepage
    driver.get(homepage_url)

    # Verify the Homepage URL is loaded
    assert homepage_url in driver.current_url, "Error: The homepage URL did not load correctly."

    # Check the API Response
    api_response = rq.get(homepage_url)
    assert api_response.status_code == 200

    # Confirm page elements are accessible (example: verify title or specific element)
    page_title = driver.title
    print(f"Page Title: {page_title}")
    assert "fitpeo" in page_title, "Error: The FitPeo homepage title is not as expected."

    # Check if a specific element (like the logo) is visible
    wait = WebDriverWait(driver, 5)
    logo_element  = wait.until(ec.presence_of_element_located((By.XPATH, "//img[@alt='FitPeo']")))

    assert logo_element.is_displayed(), "Error: The FitPeo logo is not displayed on the homepage."

    print("Test Passed: The FitPeo homepage is accessible and functioning correctly.")

    # Click on the Revenue Calculator on HomePage and Navigate to Revenue Calculator Page
    revenue_page = driver.find_element(By.XPATH, "//div[text() = 'Revenue Calculator']")
    revenue_page.click()
    revenue_element = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='MuiBox-root css-rfiegf']/h4")))
    print(revenue_element.text)

    assert revenue_element.is_displayed(), "Error: The revenue page is not loaded"

    #use execute_script to scroll to the selected element
    scroll_element = driver.find_element(By.XPATH, "//div[@class='MuiBox-root css-19zjbfs']")
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)

    time.sleep(2)

except AssertionError:
    error  = "Please check the code there is a mistake in your code"
    print(f"Test Failed: {error}")

except WebDriverException as e:
    print(f"WebDriver Error: {e}")

finally:
    # Close the Browser
    driver.quit()





