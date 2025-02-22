import time
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------------
# Instead of a hardcoded group name, prompt the user for a chat keyword (case-insensitive)
chat_keyword = input("Enter the keyword for the chat to search (case-insensitive): ").strip()
if not chat_keyword:
    print("No keyword provided. Exiting.")
    sys.exit(1)

POLL_INTERVAL = 5  # Seconds between checking for new messages

# Specify a directory for your persistent Chrome user data.
# Make sure this folder exists (or will be created) in a location your user account can write to.
USER_DATA_DIR = r"C:\Users\hssod\whatsapp_profile"

# --------------------------------------------------------------------------------
# SET UP SELENIUM WITH A PERSISTENT CHROME PROFILE
# --------------------------------------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={USER_DATA_DIR}")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
# Uncomment the next line for headless mode if desired:
# options.add_argument('--headless')

# NOTE: Update this to your ChromeDriver path if not using webdriver-manager
CHROME_DRIVER_PATH = r"C:\WebDrivers\chromedriver.exe"

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(15)  # Implicitly wait up to 15 seconds for elements

# Increase explicit wait timeout to 120 seconds to allow ample time for scanning QR code and page load
wait = WebDriverWait(driver, 120)

# --------------------------------------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------------------------------------
def save_url(url):
    """Append each found LinkedIn URL to a file."""
    with open("linkedin_urls.txt", "a") as f:
        f.write(url + "\n")

def search_and_open_chat(keyword):
    """
    Automatically search for and open the chat whose title contains the given keyword.
    Uses XPath 'contains' to match the chat title.
    """
    try:
        # Click the search button to open the search bar
        search_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='Search or start new chat']")))
        search_button.click()
        
        # Wait for the search input to appear
        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys(keyword)
        
        # Wait until a chat whose title contains the keyword is visible and click it.
        # The 'contains()' XPath function is used instead of an exact match.
        result = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(@title, '{keyword}')]")))
        result.click()
        return True
    except (NoSuchElementException, TimeoutException) as e:
        print("Error finding chat via search:", e)
        return False

def manual_chat_selection():
    """
    Fallback: Ask the user to manually open the target chat.
    Once you've manually opened the chat in WhatsApp Web, press Enter to continue.
    """
    print("Could not automatically find the chat.")
    print("Please manually open the target chat in WhatsApp Web, then press Enter to continue...")
    input()

# --------------------------------------------------------------------------------
# MAIN SCRIPT
# --------------------------------------------------------------------------------
try:
    # 1. Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    print("Waiting for WhatsApp Web to load... (On first run, please scan the QR code.)")
    
    # Wait for the main chat pane to appear. The element with id "pane-side" is usually present once logged in.
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']")))
        print("Logged in successfully! (Your session is now saved in your profile.)")
    except TimeoutException:
        print("Timeout waiting for the chat pane. Ensure you scanned the QR code.")
        print("Still not logged in. Exiting.")
        driver.quit()
        sys.exit(1)
    
    # Debug: Print currently visible chats
    print("Currently visible chats:")
    visible_chats = driver.find_elements(By.XPATH, "//span[@data-testid='chat-title']")
    for chat in visible_chats:
        print(" -", chat.text)
        
    # 2. Automatically search and open the target chat using the user-provided keyword
    if not search_and_open_chat(chat_keyword):
        print(f"Could not automatically find a chat containing '{chat_keyword}'.")
        manual_chat_selection()

    # 3. Monitor the chat for LinkedIn URLs
    linkedin_pattern = r"(https?://(?:www\.)?linkedin\.com/\S+)"
    processed_messages = set()

    print("Monitoring chat for LinkedIn URLs. Press Ctrl+C to exit.")
    while True:
        messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in, div.message-out")
        for msg in messages:
            text = msg.text
            if text not in processed_messages:
                processed_messages.add(text)
                urls = re.findall(linkedin_pattern, text)
                if urls:
                    for url in urls:
                        print("Found LinkedIn URL:", url)
                        save_url(url)
        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("Script terminated by user (Ctrl+C).")
except WebDriverException as e:
    print("WebDriverException occurred:", e)
finally:
    driver.quit()
