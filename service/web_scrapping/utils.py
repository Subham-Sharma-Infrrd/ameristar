# Detect if the page contains the relevant table headers

import random
import time

from log import logger
from model.mapping import WebScrappingWebPageTypes
from service.web_scrapping.constants import EXPECTED_HEADERS
from utils.common_utils import is_fuzzy_match
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




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
            print("reCAPTCHA iframe detected.")
            
            # Switch to the reCAPTCHA iframe
            driver.switch_to.frame(recaptcha_iframe)
            print("Switched to reCAPTCHA iframe.")
            
            # Wait for the reCAPTCHA to complete or solve it manually if required
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
            )
            print("reCAPTCHA completed or is no longer blocking.")
            
            # Switch back to the main content
            driver.switch_to.default_content()
            print("Switched back to main content. handle_captcha_first_time")

            return True
    except Exception as e:
        print(f"Error handling reCAPTCHA: {e}")
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
            print("CAPTCHA handling failed.")
            return False
        
        # Wait for the button to become clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        
        # Scroll to and click the button
        actions = ActionChains(driver)
        actions.move_to_element(search_button).perform()  # Bring the button into view
        search_button.click()  # Click the button
        print("Button clicked successfully.")
        return True
    
    except Exception as e:
        print(f"Error handling reCAPTCHA or clicking the button {e}")
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
        print("Switched to reCAPTCHA iframe.")

        # Locate the checkbox
        captcha_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox"))
        )
        print("Located reCAPTCHA checkbox.")

        # Simulate human-like mouse movement to the checkbox
        human_like_mouse_movements(driver, captcha_checkbox)

        # Simulate a slight delay before clicking
        time.sleep(random.uniform(1, 3))

        # Click the checkbox
        captcha_checkbox.click()
        print("Clicked on the reCAPTCHA checkbox.")

        # Wait for CAPTCHA resolution or invisibility
        time.sleep(random.uniform(5, 10))  # Simulate delay in CAPTCHA processing
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element((By.XPATH, recaptcha_iframe_xpath))
        )
        print("CAPTCHA resolved or is no longer blocking.")

        driver.switch_to.default_content()
        return True

    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")
        driver.switch_to.default_content()
        return False

def get_unique_id_for_tax_doc(driver, config) -> bool:
    """
    This function is to pick account_id from cad to tax document
    """
    element_path = config["xpaths"]["account_number_xpath"]
    unique_id_for_tax = get_element_value(driver, element_xpath=config["xpaths"]["unique_id_for_tax"])
    # TODO: Need to check if the unique_id_for_tax is present in the tax document


def get_element_value(driver, element_xpath, attribute=None):
    """
    Fetches the text or a specific attribute value of an element from a web page.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element_xpath (str): The XPath of the target element.
        attribute (str, optional): The attribute whose value needs to be fetched. Defaults to None (fetches text content).
    
    Returns:
        str: The value of the element's text or attribute, or None if the element is not found.
    """
    try:
        # Wait for the element to be present and visible
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        # Fetch and return the attribute value or the text content
        if attribute:
            return element.get_attribute(attribute)
        else:
            return element.text
    except Exception as e:
        print(f"Error fetching value for element with XPath '{element_xpath}': {e}")
        return None