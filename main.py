
# Example usage:
from service.web_scrapping.web_scrapper import WebScraper


if __name__ == "__main__":
    scraper = WebScraper()
    
    try:
        # Captcha Issue
        #_____________________________
        state = "TX"
        county = "HIDALGO"
        street_number = "1815"
        street_name = "KENNEDY ST"
        owner_name = "NELSON MICHAEL A & LYNDA NELSON"

        # state = "TX"
        # county = "WISE"
        # street_number = "6101"
        # street_name = "BROOKHOLLOW DR"
        # owner_name = "JOHNSON AVIS E JR"
        
        # ______________________________________

        # state = "TX"
        # county = "DENTON"
        # street_number = "16361"
        # street_name = "FM 1173"
        # owner_name = "MCDUFFIE, JOHN & KIMBERLY"

        # state = "TX"
        # county = "JOHNSON"
        # street_number = "516"
        # street_name = "CRAWFORD DR"
        # owner_name = "HILDRETH CHRISTIAN ETVIR CAMERON"
        
        # Workflow
        web_page_config = scraper.navigate_to_website(state, county)
        status = scraper.cad_perform_search(web_page_config, street_number, street_name, owner_name)
        if status:
            scraper.download_or_screenshot(web_page_config["xpaths"])
            print("SUCCESSFULLY_SCRAPPED")
        else:
            print("SCRAPPING_FAILED")
    
    finally:
        scraper.close()
