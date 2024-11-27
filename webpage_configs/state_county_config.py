COUNTER = 4
SLEEP_TIME = 5
TAX_KEYWORDS = [
  'Tax Estimator',
  'tax', 'taxes', 'taxation', 'income tax', 'tax return', 'tax form',
  'irs', 'vat', 'gst', 'revenue', 'deductions', 'taxpayer', 'filing',
  'audit', 'fiscal', 'exemption'
]

SINGLE_CLICK_PRINT_COUNTY = [
  "DENTON", "JOHNSON", "WISE"
]

DOUBLE_CLICK_PRINT_COUNTY = [
  "MCLENNAN"
]

STATE_COUNTY_CONFIG = {
  "TX": {
    "DENTON": {
      "website": "https://taxweb.dentoncounty.gov/",
      "tax_page_additional_url": "Accounts/AccountDetails?taxAccountNumber=",
      "xpaths": {
        "view_more_xpath": """//*[@id="account-view-more-collapse-down"]""",
        "e_statement_xpath": """//*[@id="account-details-header"]/div/div[2]/div[5]/a"""
      }
    },
    "JOHNSON": {
      "website": "https://www.johnsoncountytaxoffice.org/",
      "tax_page_additional_url": "Accounts/AccountDetails?taxAccountNumber=",
      "xpaths": {
        "view_more_xpath": """//*[@id="account-view-more-collapse-down"]""",
        "e_statement_xpath": """//*[@id="account-details-header"]/div/div[2]/div[5]/a"""
      }
    },
    "WISE": {
      "website": "https://tax.co.wise.tx.us/",
      "tax_page_additional_url": "Accounts/AccountDetails?taxAccountNumber=",
      "xpaths": {
        "view_more_xpath": """//*[@id="account-view-more-collapse-down"]""",
        "e_statement_xpath": """//*[@id="account-details-header"]/div/div[2]/div[5]/a"""
      }
    },


    "HIDALGO": {
      "website": "https://actweb.acttax.com/",
      "tax_page_additional_url": "act_webdev/hidalgo/showdetail2.jsp?can=",
      "xpaths": {
        "e_statement_xpath": """//*[@id="account-details-header"]/div/div[2]/div[5]/a""",
        "print_current_statement_xpath": """//*[@id="pageContent"]/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td[2]/a[1]/img""",
        "click_here": """//*[@id="pageContent"]/table[2]/tbody/tr[3]/td/div/h3/a/i""",
      }
    },
    "MCLENNAN": {
      "website": "https://actweb.acttax.com/",
      "tax_page_additional_url": "act_webdev/mclennan/showdetail2.jsp?can=",
      "xpaths": {
        "e_statement_xpath": """//*[@id="account-details-header"]/div/div[2]/div[5]/a""",
        "print_current_statement_xpath": """//*[@id="pageContent"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[2]/tbody/tr[2]/td[2]/div[1]/a/div""",
        "click_here": """//*[@id="pageContent"]/table/tbody/tr/td/table/tbody/tr[2]/td/div/h3/a/i"""
      }
    }
  }
}


# STATE_COUNTY_CONFIG = {
#     "state1": {
#         "county1": {
#             "website": "https://example.com",
#             "xpaths": {
#                 "street_number": "//*[@id='street_number_input']",
#                 "street_name": "//*[@id='street_name_input']",
#                 "search_button": "//*[@id='search_button']",
#                 "download": "//*[@id='download_button']"
#             }
#         }
#     }
# }


# DENTON
  # Hit the URL
  # //*[@id="localized-page-container"]/div/div[2]/div[2]/div/a[1]/img ---------- Click on this button
# 
# "DENTON",
# "HIDALGO",
# "JOHNSON",
# "WISE",
# "MCLENNAN",
# "BASTROP",
# "BRAZORIA",
# "GALVESTON",
# "JEFFERSON",
# "NUECES",
# "WICHITA",
# "BELL",
# "HAYS",
# "GUADALUPE",
# "COMAL",
# "KAUFMAN",
# "BRAZOS",
# "CORYELL",
# "BURNET",
# "KENDALL",
# "COLLIN",
# "TRAVIS",
# "BEXAR",
# "FORT BEND",
# "MONTGOMERY",
# "GRAYSON",
# "COOKE",
# "ELLIS",
# "GILLESPIE",
# "WEBB",
# "ROCKWALL",
# "DALLAS",
# "TARRANT",
# "WILLIAMSON",
# "HARRIS",
# "EL PASO",
# "PARKER",
# "CAMERON",
# "LUBBOCK",
# "SMITH"