from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Replace with the path to your ChromeDriver
chrome_driver_path = 'path/to/chromedriver'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

def login_to_kick(username, password):
    driver.get('https://kick.com/login')
    
    # Wait until the login form is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    
    # Enter username
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys(username)
    
    # Enter password
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys(password)
    
    # Click login button
    login_button = driver.find_element(By.XPATH, '//button[contains(text(),"Log In")]')
    login_button.click()

    # Wait until the user is logged in (check for a specific element that appears after login)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="profile-dropdown"]'))
    )
    print("Logged in successfully!")

def follow_streamers_in_category(category_name):
    # Navigate to the category page
    driver.get(f'https://kick.com/categories/{category_name}')
    
    # Wait until the streamers list is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="stream-card"]'))
    )

    # Scroll down to load more streamers
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all follow buttons and click them
    follow_buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Follow")]')
    for button in follow_buttons:
        try:
            button.click()
            time.sleep(1)  # Small delay to avoid being flagged as a bot
        except Exception as e:
            print(f"Error clicking follow button: {e}")

    print("Followed all streamers in the category!")

# Replace these with your Kick username and password
username = 'your_username'
password = 'your_password'

login_to_kick(username, password)
follow_streamers_in_category('Retro Games')

driver.quit()
