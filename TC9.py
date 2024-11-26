import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import requests as rq

# Test Data
homepage_url = "https://www.fitpeo.com"

# Set up WebDriver
try:
    # Set the path of the web browser
    Options = webdriver.ChromeOptions()
    Options.add_argument("--start-maximized")
    Options.add_argument("--disable-javascript")  # Disables JavaScript in the browser
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
    assert "fitpeo" in page_title.lower(), "Error: The FitPeo homepage title is not as expected."

    # Check if a specific element (like the logo) is visible
    wait = WebDriverWait(driver, 5)
    logo_element = wait.until(ec.presence_of_element_located((By.XPATH, "//img[@alt='FitPeo']")))

    assert logo_element.is_displayed(), "Error: The FitPeo logo is not displayed on the homepage."

    print("Test Passed: The FitPeo homepage is accessible and functioning correctly.")

    # Click on the Revenue Calculator on HomePage and Navigate to Revenue Calculator Page
    revenue_page = driver.find_element(By.XPATH, "//div[text() = 'Revenue Calculator']")
    revenue_page.click()
    revenue_element = wait.until(
        ec.presence_of_element_located((By.XPATH, "//div[@class='MuiBox-root css-rfiegf']/h4")))
    print(revenue_element.text)

    assert revenue_element.is_displayed(), "Error: The revenue page is not loaded"

    # Scroll into view and set the slider value first
    scroll_element = driver.find_element(By.XPATH, "//div[@class='MuiBox-root css-19zjbfs']")
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)

    # Navigate to revenue slider and adjust it to the desired value (e.g., 820)
    text_field = driver.find_element(By.CSS_SELECTOR, ".MuiInputBase-inputSizeSmall")
    driver.execute_script("arguments[0].value = '820'; arguments[0].dispatchEvent(new Event('input'));", text_field)

    # Optional: Trigger change event to simulate the user change
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", text_field)

    time.sleep(2)  # Give time for JavaScript to process the change

    # Now select the CPT codes after setting the slider value
    cpt_data = driver.find_elements(By.CSS_SELECTOR, ".MuiTypography-root")
    cpt_list = ["CPT-99091", "CPT-99454", "CPT-99474"]

    for data in cpt_data:
        cpt_text = data.text  # Gets the text of the current element
        if cpt_text in cpt_list:  # Check if the text matches any CPT in the list
            try:
                checkbox = data.find_element(By.XPATH, "./following::input[@type='checkbox'][1]")
                # Check if the checkbox is not already selected
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"Selected checkbox for CPT: {cpt_text}")
                else:
                    print(f"Checkbox for CPT: {cpt_text} was already selected.")
            except Exception as e:
                print(f"Error clicking checkbox for CPT: {cpt_text}, Error: {e}")

    driver.get_screenshot_as_file("Testcase9.png")

    time.sleep(2)  # Ensure all actions have been processed before continuing

except AssertionError as e:
    print(f"Test Failed: {e}")

except WebDriverException as e:
    print(f"WebDriver Error: {e}")

finally:
    # Close the Browser
    driver.quit()
