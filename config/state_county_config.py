from config.xpath_configs.xpaths_config import BASTROP_UI


STATE_COUNTY_CONFIG = {
    "TX": {
        "DENTON": {
            "CAD": {
                "website": "https://esearch.dentoncad.com/",
                "xpaths": BASTROP_UI,
                "is_captcha_present": False,
            },
            "TAX": {
                "website": "https://esearch.fbcad.org/",
                "xpaths": {},
            },
        },
        "HIDALGO": {
            "CAD": {
                "website": "https://esearch.hidalgoad.org/",
                "xpaths": BASTROP_UI,
                "is_captcha_present": True,
            },
            "TAX": {
                "website": "https://esearch.collincad.org/",
                "xpaths": {},
            },
        },
        "JOHNSON": {
            "CAD": {
                "website": "https://esearch.johnsoncad.com/",
                "xpaths": BASTROP_UI,
                "is_captcha_present": False,
            },
            "TAX": {
                "website": "https://esearch.collincad.org/",
                "xpaths": {},
            },
        },
        "WISE": {
            "CAD": {
                "website": "https://esearch.wise-cad.com/",
                "xpaths": BASTROP_UI,
                "is_captcha_present": True,
            },
            "TAX": {
                "website": "https://esearch.collincad.org/",
                "xpaths": {},
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
