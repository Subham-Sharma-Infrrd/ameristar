STATE_COUNTY_CONFIG = {
    "state1": {
        "county1": {
            "website": "https://esearch.fbcad.org/",
            "xpaths_present": {
                "address_search_button": """//*[@id="home-page-tabs"]/li[3]/a""",
                "street_number": """//*[@id="StreetNumber"]""",
                "street_name": """//*[@id="StreetName"]""",
                "search_button": """//*[@id="index-search"]/div[4]/div/div/button""",
                "search_result_table": """//*[@id="resultListDiv"]/tr""",
                "owner_name_in_search_result": """.//span[contains(@class, '_ownerName')]""",
                "download": """//a[@onclick="onPrintClick('printSummaryView')" and text()='Print Summary View']"""
            }
        }
    },
    "TX": {
        "COLLIN": {
            "website": "https://esearch.collincad.org/",
            "xpaths_present": {
                "address_search_button": """//a[@data-filter="search-address"]""",
                "street_number": """//*[@id="StreetNumber"]""",
                "street_name": """//*[@id="StreetName"]""",
                "search_button": """//button[@type="button" and @onclick="AdvancedSearch();" and @class="btn btn-default" and @value="Search"]""",
                "search_result_table": """//*[@id="resultListDiv"]/tr""",
                "owner_name_in_search_result": """.//span[contains(@class, '_ownerName')]""",
                "download": """//a[@onclick="onPrintClick('printSummaryView')" and text()='Print Summary View']"""
            }
        }
    }
    }

