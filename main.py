import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")

# Automatically fetch the correct ChromeDriver version
service = Service(ChromeDriverManager().install())

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the CAPTCHA solver function
def solve_captcha():
    try:
        # Wait for the CAPTCHA image to load
        captcha_img_xpath = "//img[@class='img-thumbnail card-img-top border-0']"
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, captcha_img_xpath))
        )
        
        # Screenshot the CAPTCHA image
        captcha_element.screenshot("captcha.png")
        print("CAPTCHA image saved as 'captcha.png'")
        
        # Solve CAPTCHA using Pytesseract
        captcha_image = Image.open("captcha.png")
        captcha_text = pytesseract.image_to_string(captcha_image, config="--oem 3 --psm 6").strip()
        print(f"CAPTCHA detected: {captcha_text}")
        
        # Enter the CAPTCHA text into the input field
        captcha_input_xpath = "//input[@class='form-control form-control-lg text-center rounded-0 remove-spaces']"
        captcha_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, captcha_input_xpath))
        )
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        print("CAPTCHA entered successfully!")
        
        # Submit the CAPTCHA form
        captcha_submit_xpath = "//button[@type='submit']"
        submit_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, captcha_submit_xpath))
        )
        submit_button.click()
        print("CAPTCHA form submitted!")
        
        # Wait for the page to reload or verify CAPTCHA
        time.sleep(3)
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")

try:
    # Open the Zefoy website
    driver.get("https://zefoy.com")
    print("Successfully opened Zefoy!")

    # Solve CAPTCHA if it exists
    solve_captcha()

    # Click heart button
    heart_xpath = "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button"
    heart_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, heart_xpath))
    )
    heart_button.click()
    print("Heart button clicked successfully!")

    # Wait for 10 seconds
    time.sleep(3)

    # Input a link into the text box
    text_box_xpath = "/html/body/div[8]/div/form/div/input"
    text_box = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, text_box_xpath))
    )
    text_box.send_keys("https://www.tiktok.com/@dgnlhcm_thaykhuong/video/7463841061853498642?lang=vi-VN")  # Replace with your desired link
    print("Link added to the text box successfully!")

    # Loop to repeat the process 10 times
    for i in range(10):
        print(f"Attempt {i + 1} of 10:")

        # Retry clicking the search button until waiting time is over
        search_xpath = "/html/body/div[8]/div/form/div/div/button"
        wait_message_xpath = "//*[contains(text(), 'Please wait')]"

        while True:
            try:
                # Click the search button
                search_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, search_xpath))
                )
                search_button.click()
                print("Search button clicked!")

                # Check for the waiting message
                wait_message_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, wait_message_xpath))
                )
                wait_message = wait_message_element.text
                print(f"Waiting message detected: {wait_message}")

                # Extract the time from the message using regex
                match = re.search(r"(\d+) minute\(s\) (\d+) second\(s\)", wait_message)
                if match:
                    minutes = int(match.group(1))
                    seconds = int(match.group(2))
                    wait_time = minutes * 60 + seconds + 5  # Add a buffer of 5 seconds
                    print(f"Waiting for {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Unable to extract wait time. Waiting for a default of 15 seconds...")
                    time.sleep(5)
            except Exception as e:
                print("No waiting message detected. Proceeding.")
                break

        # Click the submit button
        submit_xpath = "/html/body/div[8]/div/div/div[1]/div/form/button"
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, submit_xpath))
            )
            submit_button.click()
            print("Submit button clicked successfully!")
        except Exception as e:
            print(f"Error clicking the submit button: {e}")

        # Wait for a few seconds before the next iteration
        time.sleep(5)

finally:
    input("Nhấn Enter để đóng")
    driver.quit()
