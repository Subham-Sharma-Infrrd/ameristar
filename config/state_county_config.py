from config.xpath_configs.xpaths_config import BASTROP_UI


STATE_COUNTY_CONFIG = {
    "TX": {
        "DENTON": {
            "CAD": {
                "website": "https://esearch.dentoncad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "account_number_path": """//th[text()='Property ID:']/following-sibling::td"""
                },
                "account_number_patterns": [
                    r"(?i)property\s+id\s*:(\d{6})",
                ],
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://taxweb.dentoncounty.gov/Accounts/AccountDetails?taxAccountNumber={}DEN""",
                "xpaths": {
                    "view_more": """//*[@id="account-view-more-collapse-link"]""",
                    "toggle_down": """//*[@id="account-property-tax-record-{}-chevron"]""",
                    "all_year": """//*[@id="display-year-by-form"]/div/form-group/label[3]""",
                    "payment_history": """//*[@id="account-property-tax-record-list"]/div[2]/div[3]/div/a"""
                },
            },
        },
        "HIDALGO": {
            "CAD": {
                "website": "https://esearch.hidalgoad.org/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "account_number_path": """//td[strong[contains(text(), 'Geographic ID:')]]"""
                },
                "account_number_patterns": [
                    r"(?i)geographic\s+id:\s+e(\d{4}\-\d{2}\-\d{3}\-\d{4}\-\d{2})"
                ],
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://actweb.acttax.com/act_webdev/hidalgo/showdetail2.jsp?can={}""",
                "xpaths": {
                    "expand_tax_doc": """//a[text()='Expand All']""",
                    "taxes_due_detail": """//*[@id="pageContent"]/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td[2]/h3[8]/a[2]""",
                },
            },
        },
        "JOHNSON": {
            "CAD": {
                "website": "https://esearch.johnsoncad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "account_number_path": """//td[strong[contains(text(), 'Geographic ID:')]]""",
                },
                "account_number_patterns": [
                    r"(?i)geographic\s+id:\s*(\d{3}\.\d{4}\.\d{5})"
                ],
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://www.johnsoncountytaxoffice.org/Accounts/AccountDetails?taxAccountNumber={}""",
                "xpaths": {
                    "view_more": """//*[@id="account-view-more-collapse-link"]""",
                    "toggle_down": """//*[@id="account-property-tax-record-{}-chevron"]""",
                    "all_year": """//*[@id="display-year-by-form"]/div/form-group/label[3]""",
                    "payment_history": """//*[@id="account-property-tax-record-list"]/div[2]/div[3]/div/a"""
                },
            },
        },
        "WISE": {
            "CAD": {
                "website": "https://esearch.wise-cad.com/",
                "xpaths": BASTROP_UI,
                "custom_xpaths": {
                    "account_number_path": """//td[strong[contains(text(), 'Geographic ID:')]]"""
                },
                "account_number_patterns": [
                    r"(?i)property\s+id:\s*(\d{6})"
                ],
                "is_captcha_present": False,
            },
            "TAX": {
                "website": """https://tax.co.wise.tx.us/Accounts/AccountDetails?taxAccountNumber={}""",
                "xpaths": {
                    "view_more": """//*[@id="account-view-more-collapse-link"]""",
                    "toggle_down": """//*[@id="account-property-tax-record-{}-chevron"]""",
                    "all_year": """//*[@id="display-year-by-form"]/div/form-group/label[3]""",
                    "payment_history": """//*[@id="account-property-tax-record-list"]/div[2]/div[3]/div/a"""
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