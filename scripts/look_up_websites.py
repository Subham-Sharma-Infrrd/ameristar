import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from service.web_scrapping.web_scrapper import *
from webpage_configs.state_county_config import *


### Function to get and modify the URL
def get_and_modify_url_(state, county, taxAccountNumber):
  webpage_url = STATE_COUNTY_CONFIG.get(state).get(county).get("website")
  additional_url = STATE_COUNTY_CONFIG.get(state).get(county).get("tax_page_additional_url")
  return webpage_url+additional_url+taxAccountNumber


def get_clickable_xpaths(state, county, driver):
  try:
    actions = ActionChains(driver)
    actions.move_to_element(driver)
    
    if county in SINGLE_CLICK_PRINT_COUNTY:
      # Naving to the final page where the print page exists.
      element = driver.find_element(By.XPATH, STATE_COUNTY_CONFIG.get(state).get(county).get("xppaths")["e_statement_xpath"])
      # Click on the final button
      element.click()
      # wait for some second to get the final page
      time.sleep(SLEEP_TIME)

    elif county in DOUBLE_CLICK_PRINT_COUNTY:
      # Navingating to another page for this county tax page.
      element = driver.find_element(By.XPATH, STATE_COUNTY_CONFIG.get(state).get(county).get("xpaths")["print_current_statement_xpath"])
      element.click()
      time.sleep(SLEEP_TIME)
      element = driver.find_element(By.XPATH, STATE_COUNTY_CONFIG.get(state).get(county).get("xpaths")["click_here"])
      element.click()
      time.sleep(SLEEP_TIME)

  except Exception as e:
    logger.log("An exception occured while clicking on final page button {e}")

  return driver

def find_webpage_type(state, county, taxAccountNumber):
  ### 1. Get the URL in a function.
  ### 2. Modify the url as per your choice.
  ### 3. Hit the url through selenium.
  ### 4. Check getting view more clickable option through xpath as view_more_xpath in constants, click on it again and again till it comes.
  ### 5. Check weather it is a TAX document or not, if tax call download function.
  ### 6. If this is not a TAX document, than go to step 3, for atleast 5 times.
  ### Setting up the driver to get the webscrapping done.
  
  driver = WebScraper()
  ### This needs to modify as per the required details.
  tax_page_url = get_and_modify_url_(state, county, taxAccountNumber)
  
  ### Encountring this to refresh the page.
  counter = COUNTER
  while counter:
    counter -= 1

    driver.navigate_to_website_tax(tax_page_url)
    
    ### Opening the webpage completely
    VIEW_MORE_XPATH = STATE_COUNTY_CONFIG.get(state).get(county).get("view_more_xpath")
    if VIEW_MORE_XPATH:
      while True:
        try:
          view_more_button = driver.find_tax_element(VIEW_MORE_XPATH)
          view_more_button.click()
          time.sleep(2)  
          
        except (NoSuchElementException, ElementNotInteractableException):
          print("No more 'View More' buttons to click.")
          break
  
    page_raw_text = None
    ### Getting the raw text from the page with the help of selenium web driver.
    try:
      ### Wait for a specific element if provided
      WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, None))
      )
      ### Extract the body text
      page_raw_text = driver.get_raw_text(None)
      page_raw_text = driver.get_raw_text_tax(By.TAG_NAME, "body").text
      return page_raw_text.strip()
    
    except Exception as e:
      print(f"An error occurred while getting raw text: {e}")

    if not page_raw_text:
      continue

    # Check if any tax-related keywords are present in the page text
    for keyword in TAX_KEYWORDS:
      if keyword in page_raw_text:
        ### Call download or screenshot function in WebScrapper Class
        get_clickable_xpaths(state, county, driver)
        driver.download_or_screenshot("")
        driver.close()
        return

  ### If no tax-related keywords are found, even after refreshing the page, it's not a tax page
  return
