import pywhatkit as kit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service

def create_headless_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')


    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def send_whatsapp_message(phone_number, message):
    # Ensure pywhatkit uses the Selenium driver
    driver = create_headless_driver()

    # Send message using pywhatkit
    kit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=20, tab_close=True)

    # Allow some time for the message to be sent
    time.sleep(30)

    # Close the headless browser
    driver.quit()

if __name__ == "__main__":
    # Example usage
    phone_number = "+917558203692"
    message = "Hello from an automated script!"
    send_whatsapp_message(phone_number, message)
