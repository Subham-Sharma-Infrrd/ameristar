import os
import time
import base64
import logging
from PIL import Image
from io import BytesIO
from PyPDF2 import PdfMerger
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    WebDriverException
)
from selenium.webdriver.chrome.service import Service
from service.web_scrapping.web_scrapper import *

# Import configurations
from config.state_county_config import *
from config.driver_config import HEADLESS, IMPLICIT_WAIT
from constants import HTML_DIR, PDF_DIR
from log import logger
from model.mapping import WebScrappingDocType, WebScrappingWebPageTypes, WebSurfMode
from utils.web_scrapping_utils import detect_cad_homepage_page, detect_property_results_page, get_unique_id_for_tax_doc, handle_captcha_first_time, handle_recaptcha_and_click_button, initialize_stealth_driver, simulate_human_like_behavior_to_solve_captcha
from utils.common_utils import generate_unique_id
from webdriver_manager.chrome import ChromeDriverManager
from config.tax_word_configs import TAX_KEYWORDS


class WebScraper:
    def __init__(self, mode:str = WebSurfMode.STEALTH.value):
        """
        Initialize the WebScraper with external configurations.
        """
        self.mode = mode.upper()
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, IMPLICIT_WAIT)
        self.create_directories()


    def setup_driver(self):
        """
        Configure and initialize the Selenium WebDriver.
        """
        if self.mode == WebSurfMode.STEALTH.value:
            logger.info("Initializing WebDriver in stealth mode.")
            return initialize_stealth_driver()
        elif self.mode == WebSurfMode.NORMAL.value:
            logger.info("Initializing WebDriver in normal mode.")
            options = webdriver.ChromeOptions()
            if HEADLESS:
                options.add_argument("--headless=new")
            return webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            raise ValueError("Invalid mode. Use 'normal' or 'stealth'.")


    def create_directories(self):
        """
        Create directories for HTML and PDF storage if they do not exist.
        """
        os.makedirs(HTML_DIR, exist_ok=True)
        os.makedirs(PDF_DIR, exist_ok=True)


    def detect_page_type(self, web_page_config):
        """
        Detect the type of the current webpage based on validation parameters.

        Args:
            page_config (dict): A dictionary containing webpage types and their validation parameters.

        Returns:
            str: The detected page type (e.g., "HOMEPAGE", "SEARCH_RESULT_TABLE_PAGE").
            None: If no page type can be determined.
        """
        try:
            for page_type, config in web_page_config["xpaths"].items():
                validation_params = config.get("VALIDATION_PARAMS", {})

                # Check if all validation elements are present on the current page
                all_elements_present = all(
                    self.driver.find_elements(By.XPATH, xpath)
                    for xpath in validation_params.values()
                )

                if all_elements_present:
                    logger.info(f"{page_type} detected.")
                    return page_type

                if (
                    not all_elements_present
                    and page_type == WebScrappingWebPageTypes.HOMEPAGE.value
                ):
                    if detect_cad_homepage_page(self.driver, web_page_config):
                        logger.info(f"{page_type} detected.")
                        return page_type

                if (
                    not all_elements_present
                    and page_type
                    == WebScrappingWebPageTypes.SEARCH_RESULT_TABLE_PAGE.value
                ):
                    if detect_property_results_page(self.driver, config):
                        logger.info(f"{page_type} detected.")
                        return page_type

        except Exception as e:
            logger.error(f"Error detecting page type: {e}")

        logger.info("Unable to determine the current page.")
        return None


    def get_cad_configs(self, state, county):
        """
        Navigate to the website based on the state and county.
        """
        state_info = STATE_COUNTY_CONFIG.get(state.upper())
        if not state_info:
            raise ValueError(f"No configuration found for state: {state}")

        county_info = state_info.get(county.upper())
        if not county_info:
            raise ValueError(
                f"No configuration found for county: {county} in state: {state}"
            )

        cad_county_info = county_info.get(WebScrappingDocType.CAD.value)
        if not cad_county_info:
            raise ValueError(
                f"No configuration found for county: {county} in state: {state}"
            )
        return cad_county_info


    def get_tax_configs(self, state, county):
        """
        Navigate to the website based on the state and county.
        """
        state_info = STATE_COUNTY_CONFIG.get(state.upper())
        if not state_info:
            raise ValueError(f"No configuration found for state: {state}")

        tax_info = state_info.get(county.upper())
        if not tax_info:
            raise ValueError(
                f"No configuration found for county: {county} in state: {state}"
            )

        tax_county_info = tax_info.get(WebScrappingDocType.TAX.value)
        if not tax_county_info:
            raise ValueError(
                f"No configuration found for county: {county} in state: {state}"
            )
        return tax_county_info


    def cad_perform_search(self, xpaths_configs, street_number, street_name, owner_name):
        """
        Perform a search and navigate to the relevant result.
        """
        try:
            self.driver.get(xpaths_configs["website"])
            for attempt in range(5):  # Retry up to 3 times
                page_type = self.detect_page_type(xpaths_configs)
                xpaths = xpaths_configs.get("xpaths", {}).get(page_type)
                if xpaths_configs['is_captcha_present']:
                    simulate_human_like_behavior_to_solve_captcha(self.driver)
                if page_type == WebScrappingWebPageTypes.HOMEPAGE.value:
                    logger.info("Filling out the search form.")
                    if xpaths_configs['is_captcha_present']:
                        handle_captcha_first_time(self.driver)
                    # Click the address search button
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, xpaths["address_search_button"])
                        )
                    ).click()
                    logger.info("clicked on address search button")
                    time.sleep(10)
                    # Fill in search inputs
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, xpaths["street_number"])
                        )
                    ).send_keys(street_number)

                    logger.info("updated on street number")
                    time.sleep(10)
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, xpaths["street_name"])
                        )
                    ).send_keys(street_name)
                    time.sleep(10)

                    logger.info("Updated Street Name")
                    if xpaths_configs['is_captcha_present'] and handle_recaptcha_and_click_button(self.driver, xpaths["search_button"]):
                        logger.info("Operation completed successfully.")
                    elif not xpaths_configs['is_captcha_present']:
                        # Click the search button
                        self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, xpaths["search_button"]))
                        ).click()
                        time.sleep(10)
                    else:
                        logger.info("Operation failed.")
                    time.sleep(10)
                    logger.info("CLicked on Search Button")
                    continue

                elif (
                    page_type == WebScrappingWebPageTypes.SEARCH_RESULT_TABLE_PAGE.value
                ):
                    logger.info("Checking search results.")
                    # Get search result rows
                    rows = self.driver.find_elements(
                        By.XPATH, xpaths.get("search_result_table")
                    )
                    num_rows = len(rows)
                    logger.info(f"Number of rows found: {num_rows}")

                    if num_rows == 0:
                        logger.info("No rows found. Refreshing the page.")
                        self.driver.refresh()
                        time.sleep(10)
                        continue

                    # Loop through each row to find the owner name
                    for row in rows:
                        try:
                            row_text = row.text.strip()
                            logger.info(f"Row text: {row_text}")

                            if (
                                owner_name.lower() in row_text.lower()
                            ):  # Check if owner name matches
                                logger.info(f"Owner name '{owner_name}' found in row.")
                                search_page_stage_url = self.driver.current_url
                                row.click()  # Click the matching row
                                try:
                                    # Wait for the URL to change
                                    WebDriverWait(self.driver, 30).until(
                                        EC.url_changes(search_page_stage_url)
                                    )
                                    logger.info("URL has changed. New page loaded.")
                                except Exception as e:
                                    logger.info(f"Error waiting for URL change: {e}")
                                    # Optional fallback to wait for a specific element

                        except StaleElementReferenceException:
                            logger.exception(
                                "Stale element reference detected. Re-locating rows."
                            )
                            rows = self.driver.find_elements(
                                By.XPATH, xpaths["search_result_table"]
                            )
                            continue
                elif page_type == WebScrappingWebPageTypes.SEARCH_RESULT_PAGE.value:
                    account_number = get_unique_id_for_tax_doc(self.driver, xpaths_configs)
                    return account_number

                else:
                    logger.info("Unable to determine the page type. Refreshing.")
                    self.driver.refresh()
                    time.sleep(10)

            logger.info(f"Owner name '{owner_name}' not found after {attempt + 1} attempts.")

        except NoSuchElementException as e:
            logger.exception(f"Element not found during search: {e}")
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return False
    

    def tax_page_expand_web_page(self, configs, link_to_page= None):
        """
        Clicks on the 'View More' element to reveal the complete document.

        Args:
            driver (webdriver): The Selenium WebDriver instance.
        """
        try:
            if link_to_page:
                self.driver.get(link_to_page)
                # time.sleep(5)
            # Get locators from configuration
            view_more_config = configs["view_more_button"]
            dynamic_element_config = configs["dynamic_element_to_wait"]

            # Determine locator strategy
            # if "id" in view_more_config:
            #     locator = (By.ID, view_more_config["id"])
            if "xpath" in view_more_config:
                locator = (By.XPATH, view_more_config["xpath"])
            else:
                raise ValueError("Invalid locator configuration for 'view_more_button'.")

            # Wait for the 'View More' element to be clickable
            view_more_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )

            # Scroll to the element to ensure visibility (optional)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", view_more_element)

            # Click the 'View More' button
            view_more_element.click()

            # Wait for dynamic content to load
            if "xpath" in dynamic_element_config:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, dynamic_element_config["xpath"])
                    )
                )
            logger.info("Clicked 'View More' and revealed additional content.")
        except Exception as e:
            logger.info(f"Error while clicking 'View More': {e}")


    def download_or_screenshot(self, xpaths=None, link_to_page= None, doc_type = None):
        """
        Check for download options or save a screenshot if not available.
        Save the file in the appropriate directory.
        """
        unique_id = generate_unique_id()
        if link_to_page:
            self.driver.get(link_to_page)
            time.sleep(5)
        try:
            #     # Try downloading the PDF
            #     # Wait until the element is visible
            #     print_element = WebDriverWait(self.driver, 60).until(
            #         EC.visibility_of_element_located(
            #             (By.XPATH, xpaths.get(WebScrappingWebPageTypes.SEARCH_RESULT_PAGE.value).get("PRINT_BUTTON"))
            #         )
            #     )
            #     print_element.click()
            #     print_summary_element = WebDriverWait(self.driver, 60).until(
            #         EC.visibility_of_element_located(
            #             (By.XPATH, xpaths.get(WebScrappingWebPageTypes.SEARCH_RESULT_PAGE.value).get("PRINT_SUMMARY_VIEW"))
            #         )
            #     )
            #     print_summary_element.click()
            #     logger.info("Clicked on the element.")
            # except Exception as e:
            logger.info("Download button not found. Saving screenshot.")
            # screenshot_path = os.path.join(HTML_DIR, f"{unique_id}.jpg")
            # self.driver.save_screenshot(screenshot_path)
            # logger.info(f"Screenshot saved to: {screenshot_path}")

            # Save the page as a PDF in the PDF directory
            pdf_path = os.path.join(PDF_DIR, f"{doc_type}_{unique_id}.pdf") if doc_type else os.path.join(PDF_DIR, f"{unique_id}.pdf")
            print_options = PrintOptions()
            print_options.page_width = 21
            print_options.page_height = 29
            pdf = self.driver.print_page(print_options=print_options)
            pdf_bytes = base64.b64decode(pdf)
            
            with open(pdf_path, "wb") as fh:
                fh.write(pdf_bytes)
            logger.info(f"HTML content saved as PDF to: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.exception(e)
            return None


    def navigate_to_website_tax(self, url):
        ##### This will hit the URL and direct you over there.
        try:
            self.driver.get(url)
            # Maximize the browser window (optional)
            self.driver.maximize_window()
        
        except Exception as e:
            logger.log(logging.log, f"Encountering error in opening the website: {e}")


    def get_raw_text(self):
        """
        Parameters:
            driver (webdriver): The Selenium WebDriver instance.
        Returns:
            str: The raw text of the webpage.
        """
        try:
            # Get the text of the <body> tag
            page_raw_text = self.driver.find_element(By.TAG_NAME, "body").text
            return page_raw_text.strip()
        except Exception as e:
            # Return if you are ancountring any error in getting in the raw text.
            print(f"An error occurred while getting raw text: {e}")
            return ""


    def tax_download_or_screenshot(self, doc_type):
        """
            This method will return the file_name after taking screenshots.
        """
        unique_id = generate_unique_id()
        try:
            pdf_path = os.path.join(PDF_DIR, f"{doc_type}_{unique_id}.pdf") if doc_type else os.path.join(PDF_DIR, f"{unique_id}.pdf")
            print_options = PrintOptions()
            print_options.page_width = 21
            print_options.page_height = 29
            pdf = self.driver.print_page(print_options=print_options)
            pdf_bytes = base64.b64decode(pdf)
            
            with open(pdf_path, "wb") as fh:
                fh.write(pdf_bytes)
            logger.info(f"HTML content saved as PDF to: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.exception(e)
            return None
        

    def get_all_file_merged(self, all_pdf_paths, doc_type):
        '''
            This method will merge the two pdf's or multiple into ones.
            Returns the single pdf file path that is being merged and stored.
        '''
        try:
            # Ensure the PDF directory exists
            if not os.path.exists(PDF_DIR):
                os.makedirs(PDF_DIR)
                logger.info(logging.INFO, "Creating OS DIR path")
            
            unique_id = generate_unique_id()
            # Generate the path for the final merged PDF
            pdf_path = os.path.join(
                PDF_DIR, 
                f"{doc_type}_{unique_id}.pdf" if doc_type else f"{unique_id}.pdf"
            )
            logger.info(logging.INFO, f"New PDF path created: {pdf_path}")

            # Use PdfMerger to merge all PDFs
            merger = PdfMerger()
            for pdf_path_item in all_pdf_paths:
                if os.path.exists(pdf_path_item):
                    merger.append(pdf_path_item)
                else:
                    logger.log(logging.log, f"File not found: {pdf_path_item}")
            
            # Write the merged PDF to the final path
            merger.write(pdf_path)
            merger.close()
            
            logger.log(logging.INFO, f"PDFs merged successfully into: {pdf_path}")
            return pdf_path

        except Exception as e:
            logger.error(logging.ERROR, f"Encountring the exception while merging the PDF's into ONE as: {e}")
            return None


    def is_tax_page(self):
        '''
            This will check the page, which is loaded is tax page or not
            Input:
                Driver Class object
            Output: 
                Will Return if it is 
        '''
        # Getting the raw text, to check for tax page
        page_raw_text = self.driver.find_element(By.TAG_NAME, "body").text
        page_raw_text.strip()

        if "Tax Account Number not found" in page_raw_text:
            logger.error(logging.ERROR, "Page is not loaded properly")
            return False

        # Check for TAX page
        found_tax_keywords = False
        for keyword in TAX_KEYWORDS:
            if keyword in page_raw_text:
                found_tax_keywords = True
                return True

        # If no TAX keywords are there than reload the website
        if not found_tax_keywords:
            logger.error(logging.ERROR, "Not getting any TAX related keywords on the page, reloading...!!!")
            return False


    def process_tax_page(self, config, tax_url):
        '''
            Helps in getting identification for the TAX page and to download the correct TAX page according to the STATE and COUNTY
            Parameters:
                driver object, state, county, taxAccountNumber
            Returns:
                Nothing, last call for the download function to take screenshot or download the webpage.
        '''
        counter = 3
        while counter:
            counter -= 1

            self.navigate_to_website_tax(tax_url)  
            if not self.is_tax_page():
                continue

            keyword_actions = {
                "group1": ["denton", "johnson", "wise"],
                "group2": ["hidalgo"]
            }

            for group, keywords in keyword_actions.items():
                if any(keyword in tax_url for keyword in keywords):
                    if group == "group1":
                        try: 
                            ### Opening ALL_YEARS page
                            all_year_event = self.driver.find_element(By.XPATH, config["xpaths"]["all_year"])
                            all_year_event.click()

                            ### Opening the pop-up window to take the screenshot of the page.                    
                            element = self.driver.find_element(By.XPATH, config["xpaths"]["payment_history"])
                            element.click()
                            time.sleep(3)

                            all_pdf_paths = []
                            all_pdf_paths.append(self.tax_download_or_screenshot("tax"))
                            logger.info(logging.INFO, f"Detailed taxation report: {all_pdf_paths[0]}")

                            ### Closing the pop-up window to get the view_more button
                            self.driver.refresh()

                            ### Opening the webpage completely
                            while True:
                                view_more_button = self.driver.find_element(By.XPATH, config["xpaths"]["view_more"])
                                if view_more_button.text == "Minimize":
                                    break
                                view_more_button.click()
                                time.sleep(2)  

                            ### Opening the first toggle having amount
                            current_year = datetime.now().year
                            element = self.driver.find_element(
                                By.XPATH, 
                                config["xpaths"]["toggle_down"].format(current_year)
                            )
                            element.click()
                            time.sleep(3)
                            logger.info(logging.INFO, f"Clicked on year {current_year}")

                            ### Downloading the current page after expanding all the year analysis
                            all_pdf_paths.append(self.tax_download_or_screenshot("tax"))
                            logger.info(logging.INFO, f"All year tax details: {all_pdf_paths[-1]}")

                            ### Will pick the file from the list with path of all files and merge them all
                            return self.get_all_file_merged(all_pdf_paths[::-1], "TAX")
                        
                        except (NoSuchElementException, ElementNotInteractableException):
                            logger.error(logging.ERROR, "No more 'View More' buttons to click.")
                            return None
                        
                        except Exception as e:
                            logger.error(logging.ERROR, f"An error is encountered as: {e}")
                            return None
                        
                    elif group == "group2":
                        try: 
                            self.download_or_screenshot()
                            element = self.driver.find_element(By.XPATH, config["xpaths"]["taxes_due_detail"])
                            element.click()
                        
                            # Refresh the current page
                            self.driver.refresh()
                            time.sleep(5)
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.TAG_NAME, "html"))
                            )
                            return self.tax_download_or_screenshot("TAX")
                        
                        except Exception as e:
                            logger.error(logging.ERROR, f"Encountring the error with: {e}")

            return None 


    def close(self):
        """
        Close the browser and clean up resources.
        """
        self.driver.quit()
