# Detect if the page contains the relevant table headers

import random
import re
import time

from selenium import webdriver
from config.driver_config import HEADLESS
from log import logger
from model.mapping import WebScrappingWebPageTypes
from service.web_scrapping.constants import EXPECTED_HEADERS
from utils.common_utils import is_fuzzy_match
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

def detect_cad_homepage_page(driver, validation_params):
    """
    Detect if the page is a search or results page based on URL and content
    """
    try:
        current_url = driver.current_url
        logger.info(f"Current URL: {current_url}")

        # Check for a results page based on URL structure
        if current_url == validation_params["website"]:
            logger.info("Results page URL detected.")
            return WebScrappingWebPageTypes.HOMEPAGE.value

    except Exception as e:
        logger.info(f"Error detecting property results page: {e}")
        return None


def detect_property_results_page(driver, validation_params):
    """
    Detect if the page is a search or results page based on URL and content
    """
    try:
        current_url = driver.current_url
        logger.info(f"Current URL: {current_url}")

        # Check for a results page based on URL structure
        if any (_url.lower() in current_url.lower() for _url in validation_params.get("URL_VALIDATIONS", [])):
            logger.info("Results page URL detected.")
            return WebScrappingWebPageTypes.SEARCH_RESULT_TABLE_PAGE.value

        # Get all the table header texts
        headers = driver.find_elements(By.XPATH, "//div[@id='grid' and contains(@class, 'wrap')]/table//thead//th")

        # Check if the required headers exist with fuzzy matching
        for header in headers:
            header_text = header.text
            if is_fuzzy_match(header_text, EXPECTED_HEADERS["Property ID"]) or \
               is_fuzzy_match(header_text, EXPECTED_HEADERS["Geo ID"]) or \
               is_fuzzy_match(header_text, EXPECTED_HEADERS["Owner Name"]):
                logger.info(f"Match found: {header_text}")
        
        # Check if the key headers are present
        if any(is_fuzzy_match(header.text, EXPECTED_HEADERS["Property ID"]) for header in headers) and \
           any(is_fuzzy_match(header.text, EXPECTED_HEADERS["Geo ID"]) for header in headers) and \
           any(is_fuzzy_match(header.text, EXPECTED_HEADERS["Owner Name"]) for header in headers):
            logger.info("Property Search Results page detected based on content.")
            return "property_search_results_page"
        else:
            logger.info("Not a Property Search Results page based on content.")
            return None

    except Exception as e:
        logger.info(f"Error detecting property results page: {e}")
        return None

def handle_captcha_first_time(driver, recaptcha_iframe_xpath="//iframe[contains(@title, 'reCAPTCHA')]"):
    """
    Handles CAPTCHA explicitly the first time it appears.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        recaptcha_iframe_xpath (str): The XPath of the reCAPTCHA iframe.
    
    Returns:
        bool: True if the CAPTCHA was successfully handled, False otherwise.
    """
    try:
        # Check if the reCAPTCHA iframe is present
        recaptcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, recaptcha_iframe_xpath))
        )
        if recaptcha_iframe:
            logger.info("reCAPTCHA iframe detected.")
            
            # Switch to the reCAPTCHA iframe
            driver.switch_to.frame(recaptcha_iframe)
            logger.info("Switched to reCAPTCHA iframe.")
            
            # Wait for the reCAPTCHA to complete or solve it manually if required
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
            )
            logger.info("reCAPTCHA completed or is no longer blocking.")
            
            # Switch back to the main content
            driver.switch_to.default_content()
            logger.info("Switched back to main content. handle_captcha_first_time")

            return True
    except Exception as e:
        logger.info(f"Error handling reCAPTCHA: {e}")
        return False


def handle_recaptcha_and_click_button(driver, button_xpath, recaptcha_iframe_xpath="//iframe[contains(@title, 'reCAPTCHA')]"):
    """
    Handles reCAPTCHA (if present) and clicks a specified button on the page.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        button_xpath (str): The XPath of the button to be clicked.
        recaptcha_iframe_xpath (str): The XPath of the reCAPTCHA iframe (default is for Google's reCAPTCHA).
    
    Returns:
        bool: True if the button was successfully clicked, False otherwise.
    """
    try:
        # Call the CAPTCHA handler first
        if not handle_captcha_first_time(driver, recaptcha_iframe_xpath):
            logger.info("CAPTCHA handling failed.")
            return False
        
        # Wait for the button to become clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        
        # Scroll to and click the button
        actions = ActionChains(driver)
        actions.move_to_element(search_button).perform()  # Bring the button into view
        search_button.click()  # Click the button
        logger.info("Button clicked successfully.")
        return True
    
    except Exception as e:
        logger.info(f"Error handling reCAPTCHA or clicking the button {e}")
        return False

def human_like_mouse_movements(driver, element):
    """
    Simulate human-like mouse movements to an element.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element (WebElement): The target WebElement.
    """
    actions = ActionChains(driver)
    start_x, start_y = random.randint(0, 50), random.randint(0, 50)  # Random starting position
    end_x, end_y = element.location['x'], element.location['y']  # Target element's position

    # Randomized intermediate points
    for _ in range(5):  # Adjust for smoother or rougher paths
        intermediate_x = random.randint(start_x, end_x)
        intermediate_y = random.randint(start_y, end_y)
        actions.move_by_offset(intermediate_x, intermediate_y)
        actions.pause(random.uniform(0.1, 0.5))  # Small pauses to mimic human hand delays

    actions.move_to_element(element).perform()  # Final alignment to the element


def simulate_human_like_behavior_to_solve_captcha(driver, recaptcha_iframe_xpath="//iframe[contains(@title, 'reCAPTCHA')]"):
    """
    Simulate human-like behavior to interact with reCAPTCHA.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        recaptcha_iframe_xpath (str): The XPath of the reCAPTCHA iframe.
    
    Returns:
        bool: True if CAPTCHA interaction was successful, False otherwise.
    """
    try:
        # Locate the reCAPTCHA iframe
        recaptcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, recaptcha_iframe_xpath))
        )
        driver.switch_to.frame(recaptcha_iframe)
        logger.info("Switched to reCAPTCHA iframe.")

        # Locate the checkbox
        captcha_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox"))
        )
        logger.info("Located reCAPTCHA checkbox.")

        # Simulate human-like mouse movement to the checkbox
        human_like_mouse_movements(driver, captcha_checkbox)

        # Simulate a slight delay before clicking
        time.sleep(random.uniform(1, 3))

        # Click the checkbox
        captcha_checkbox.click()
        logger.info("Clicked on the reCAPTCHA checkbox.")

        # Wait for CAPTCHA resolution or invisibility
        time.sleep(random.uniform(5, 10))  # Simulate delay in CAPTCHA processing
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element((By.XPATH, recaptcha_iframe_xpath))
        )
        logger.info("CAPTCHA resolved or is no longer blocking.")

        driver.switch_to.default_content()
        return True

    except Exception as e:
        logger.info(f"Error solving CAPTCHA: {e}")
        driver.switch_to.default_content()
        return False



def get_unique_id_for_tax_doc(driver, config, timeout=10) -> bool:
    """
    This function is to pick account_id from cad to tax document
    """
    # TODO: Need to check if the unique_id_for_tax is present in the tax document
    try:
        # Getting the text of the element from the xpath
        property_id_td = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, config["custom_xpaths"]["account_number_path"]))
        )
        text_linked = property_id_td.text
        if not text_linked:
            return None
        
        regex_patterns = config["account_number_patterns"]
        for pattern in regex_patterns:
            match = re.search(pattern, text_linked)
            if match:
                account_id = match.group(1)
                break
        
        logger.info(f"Account Number: {account_id}")
        return account_id

    except Exception as e:
        logger.info(f"Error fetching value for element with XPath': {e}")
        return None


def get_url_for_tax_docs(state, county, tax_web_page_config):
    """
    Generates the base URL for tax documents based on the provided state and county.

    Args:
        state (str): The state name.
        county (str): The county name.
        tax_web_page_config (dict): A dictionary containing URL templates for tax documents.

    Returns:
        str: The base URL for the tax documents.
    """
    try:
        # Normalize state and county to lower case for lookup
        state = state.lower().strip()
        # county = county.lower().strip()

        # Find the URL template in the configuration
        base_url = tax_web_page_config.get("website")
        if base_url is None:
            raise ValueError("Base URL template not found in the configuration.")
        
        logger.info(f"Base URL for {state.title()}, {county.title()}: {base_url}")
        return base_url
        
    except Exception as e:
        logger.info(f"Error generating base URL: {e}")
        return None


def update_tax_url_with_tax_number(base_url, account_number):
    """
    Updates the base tax URL with the provided account number.

    Args:
        base_url (str): The base URL for tax documents.
        account_number (str): The account or property ID.

    Returns:
        str: The complete URL with the account number included.
    """
    try:
        if '{}' not in base_url:
            raise ValueError("The URL does not contain a '{}' placeholder.")

        # Replace the placeholder with the account number
        updated_url = base_url.format(account_number)
        logger.info(f"Updated URL: {updated_url}")
        return updated_url

    except Exception as e:
        logger.info(f"Error updating tax URL: {e}")
        return None

def initialize_stealth_driver():
    """
    Initializes a stealth-enabled Selenium WebDriver with specified configurations.

    Returns:
        WebDriver: A configured instance of Selenium WebDriver.
    """
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")  # Use new headless mode

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Rotate user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        # Add more user agents as needed
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')

    # Set up ChromeDriver with Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Set `navigator.webdriver` to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Set user agent via CDP
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    # Enable stealth mode
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver


def update_account_number_format(state: str, county: str, text: str)-> str:
    """
    This function is to update the account number format based on the state and county
    """
    if state.upper() in ["TX"]:
        if county.upper() in ["JOHNSON"]:
            return text.replace(".", "-")
        elif county.upper() in ["HIDALGO"]:
            return text.replace("-", "")
        else:
            return text
    return text

def reveal_complete_document(driver):
    """
    Clicks on the 'View More' element to reveal the complete document.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
    """
    try:
        # Wait for the 'View More' element to be clickable
        view_more_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "account-view-more-collapse-down"))
        )

        # Scroll to the element to ensure visibility (optional)
        driver.execute_script("arguments[0].scrollIntoView(true);", view_more_element)

        # Click the 'View More' button
        view_more_element.click()

        # Allow some time for the content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*"))  # Wait for DOM update
        )

        print("Clicked 'View More' and revealed additional content.")
    except Exception as e:
        print(f"Error while clicking 'View More': {e}")
