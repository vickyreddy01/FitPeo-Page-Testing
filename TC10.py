from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Setup the webdriver (assuming you're using Chrome)
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://www.fitpeo.com/revenue-calculator")

# Wait for the page to load completely (adjust as necessary)
driver.implicitly_wait(10)

# Locate the slider input element
slider = driver.find_element(By.XPATH, '//span[contains(@class, "MuiSlider-thumb")]/input')

# Extract the slider's min and max values
min_value = int(slider.get_attribute('min'))
max_value = int(slider.get_attribute('max'))

# Get the width of the slider track element
slider_track = driver.find_element(By.XPATH, '//span[contains(@class, "MuiSlider-track")]')
slider_width = slider_track.size['width']

# Let's assume you want to move the slider by 10% of the slider width
# You can change this value to any percentage you prefer.
percentage_to_move = 57.14  # 10% move, adjust as necessary
slider_offset = slider_width * percentage_to_move

# Print the offset to ensure correct calculation
print(f"Calculated slider offset: {slider_offset}")

# Create an action chain to move the slider incrementally
actions = ActionChains(driver)

# Move the slider by the calculated offset from its current position
actions.move_to_element(slider).click_and_hold().move_by_offset(slider_offset, 0).release().perform()

# Optional: Add a sleep or wait to let the page respond to the action
time.sleep(2)

# Verify if the slider value has been set correctly
slider_value = slider.get_attribute('aria-valuenow')
print(f"Slider moved to value: {slider_value}")

# Close the driver
driver.quit()
