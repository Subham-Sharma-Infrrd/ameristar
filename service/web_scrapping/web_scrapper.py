import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Import configurations
from webpage_configs.state_county_config import STATE_COUNTY_CONFIG
from webpage_configs.driver_config import HEADLESS, IMPLICIT_WAIT
from constants import HTML_DIR, PDF_DIR
from log import logger

class WebScraper:
    def __init__(self):
        """
        Initialize the WebScraper with external configurations.
        """
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, IMPLICIT_WAIT)
        self.create_directories()

    def setup_driver(self):
        """
        Configure and initialize the Selenium WebDriver.
        """
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        
        return webdriver.Chrome(options=options)

    def create_directories(self):
        """
        Create directories for HTML and PDF storage if they do not exist.
        """
        os.makedirs(HTML_DIR, exist_ok=True)
        os.makedirs(PDF_DIR, exist_ok=True)

    def detect_page_type(self, xpaths):
        """
        Detect whether the current page is a search page or a search results page.
        Returns:
            "search_page" if the current page is a search page,
            "results_page" if the current page is a search results page,
            None if neither can be determined.
        """
        try:
            # Check for a unique element on the search page
            if self.driver.find_elements(By.XPATH, xpaths["address_search_button"]):
                logger.info("Search page detected.")
                return "search_page"

            # Check for a unique element on the search results page
            if self.driver.find_elements(By.XPATH, xpaths["search_result_table"]):
                logger.info("Search results page detected.")
                return "results_page"
        except Exception as e:
            logger.error(f"Error detecting page type: {e}")

        logger.info("Unable to determine the current page.")
        return None

    def navigate_to_website(self, state, county):
        """
        Navigate to the website based on the state and county.
        """
        state_info = STATE_COUNTY_CONFIG.get(state.lower(), STATE_COUNTY_CONFIG.get(state.upper()))
        if not state_info:
            raise ValueError(f"No configuration found for state: {state}")
        
        county_info = state_info.get(county.lower(), state_info.get(county.upper()))
        if not county_info:
            raise ValueError(f"No configuration found for county: {county} in state: {state}")
        
        self.driver.get(county_info["website"])
        return county_info["xpaths"]
    
    def navigate_to_website_tax(self, url):
      # Open the URL
      self.driver.get(url)

      # Maximize the browser window (optional)
      self.driver.maximize_window()

      return self.driver
    
    def find_tax_element(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def get_raw_text(self):
      return self.driver.get

    def perform_search(self, xpaths, street_number, street_name, owner_name):
        """
        Perform a search and navigate to the relevant result.
        """
        try:
            for attempt in range(3):  # Retry up to 3 times
                page_type = self.detect_page_type(xpaths)

                if page_type == "search_page":
                    logger.info("Filling out the search form.")
                    # Click the address search button
                    self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths["address_search_button"]))).click()

                    # Fill in search inputs
                    self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths["street_number"]))).send_keys(street_number)
                    self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths["street_name"]))).send_keys(street_name)

                    # Click the search button
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["search_button"]))).click()

                elif page_type == "results_page":
                    logger.info("Checking search results.")
                    # Get search result rows
                    rows = self.driver.find_elements(By.XPATH, xpaths["search_result_table"])
                    num_rows = len(rows)
                    logger.info(f"Number of rows found: {num_rows}")

                    if num_rows == 0:
                        logger.info("No rows found. Refreshing the page.")
                        self.driver.refresh()
                        time.sleep(3)
                        continue

                    # Loop through each row to find the owner name
                    for row in rows:
                        try:
                            row_text = row.text.strip()
                            logger.info(f"Row text: {row_text}")

                            if owner_name.lower() in row_text.lower():  # Check if owner name matches
                                logger.info(f"Owner name '{owner_name}' found in row.")
                                row.click()  # Click the matching row
                                return  # Exit after successful click

                        except StaleElementReferenceException:
                            logger.exception("Stale element reference detected. Re-locating rows.")
                            rows = self.driver.find_elements(By.XPATH, xpaths["search_result_table"])
                            continue

                else:
                    logger.info("Unable to determine the page type. Refreshing.")
                    self.driver.refresh()
                    time.sleep(3)

            logger.info(f"Owner name '{owner_name}' not found after {attempt + 1} attempts.")

        except NoSuchElementException as e:
            logger.exception(f"Element not found during search: {e}")
        except Exception as e:
            logger.exception(f"An error occurred: {e}")

    def download_or_screenshot(self, xpaths):
        """
        Check for download options or save a screenshot if not available.
        Save the file in the appropriate directory.
        """
        timestamp = int(time.time())
        try:
            # Try downloading the PDF
            # Wait until the element is visible
            element = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@onclick=\"onPrintClick('printSummaryView')\"]"))
            )
            element.click()
            logger.info("Clicked on the element.")
        except Exception as e:
            # logger.info("Download button not found. Saving screenshot.")
            # screenshot_path = os.path.join(HTML_DIR, f"{timestamp}.jpg")
            # self.driver.save_screenshot(screenshot_path)
            # logger.info(f"Screenshot saved to: {screenshot_path}")
            
            # Save the page as a PDF in the PDF directory
            pdf_path = os.path.join(PDF_DIR, f"{timestamp}.pdf")
            print_options = PrintOptions()
            print_options.page_width = 21
            print_options.page_height = 29
            pdf = self.driver.print_page(print_options=print_options)
            pdf_bytes = base64.b64decode(pdf)
            with open(pdf_path, "wb") as fh:
                fh.write(pdf_bytes)
            logger.exception(f"HTML content saved as PDF to: {pdf_path}")
        except Exception as e:
            logger.error(e)

    def close(self):
        """
        Close the browser and clean up resources.
        """
        self.driver.quit()


# Example usage:
if __name__ == "__main__":
    scraper = WebScraper()
    
    try:
        state = "TX"
        county = "COLLIN"
        street_number = "9900"
        street_name = "PRESTON VINEYARD"
        owner_name = "JOHNSON GENE &"
        
        # Workflow
        xpaths = scraper.navigate_to_website(state, county)
        scraper.perform_search(xpaths, street_number, street_name, owner_name)
        scraper.download_or_screenshot(xpaths)
    
    finally:
        scraper.close()