from config.xpath_configs.xpaths_config import BASTROP_UI


STATE_COUNTY_CONFIG = {
    "TX": {
        "DENTON": {
            "CAD": {
                "website": "https://esearch.dentoncad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "ACCOUNT_NUMBER_PATH": """//th[text()='Property ID:']/following-sibling::td"""
                },
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://taxweb.dentoncounty.gov/Accounts/AccountDetails?taxAccountNumber={}DEN""",
                "xpaths": {},
            },
        },
        "HIDALGO": {
            "CAD": {
                "website": "https://esearch.hidalgoad.org/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "ACCOUNT_NUMBER_PATH": """//td[strong[contains(text(), 'Geographic ID:')]]"""
                },  # Custom xpaths for Hidalgo CAD
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://actweb.acttax.com/act_webdev/hidalgo/showdetail2.jsp?can={}""",
                "xpaths": {
                    "expand_tax_doc": """//a[text()='Expand All']""",
                },
            },
        },
        "JOHNSON": {
            "CAD": {
                "website": "https://esearch.johnsoncad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "ACCOUNT_NUMBER_PATH": """//td[strong[contains(text(), 'Geographic ID:')]]"""
                },
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://www.johnsoncountytaxoffice.org/Accounts/AccountDetails?taxAccountNumber={}""",
                "xpaths": {
                    "expand_tax_doc": """//a[text()='Expand All']""",
                },
            },
        },
        "WISE": {
            "CAD": {
                "website": "https://esearch.wise-cad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "ACCOUNT_NUMBER_PATH": """//td[strong[contains(text(), 'Geographic ID:')]]"""
                },
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://tax.co.wise.tx.us/Accounts/AccountDetails?taxAccountNumber={}""",
                "xpaths": {
                    "expand_tax_doc": """//a[text()='Expand All']""",
                },
            },
        },
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
#     },
#     "state2": {
#         "county2": {
#             "website": "https://example2.com",
#             "xpaths": {
#                 "street_number": "//*[@id='street_number']",
#                 "street_name": "//*[@id='street_name']",
#                 "search_button": "//*[@id='submit_button']",
#                 "download": "//*[@id='file_download']"
#             }
#         }
#     }
# }
