BASTROP_UI = {
        "HOMEPAGE": {
            # "URL_VALIDATIONS": "https://esearch.fbcad.org/",
            "VALIDATION_PARAMS": {
                "address_search_button": """//a[@data-filter="search-address" and contains(normalize-space(text()), "By Address")]""",
                # "street_number": """//input[contains(@class, "form-control") and @id="StreetNumber" and @name="StreetNumber" and @type="text"]""",
                # "street_name": """//input[contains(@class, "form-control") and @id="StreetName" and @name="StreetName" and @type="text"]""",
                "search_button": """//button[@type="button" and contains(@onclick, "AdvancedSearch") and contains(@class, "btn btn-default") and contains(normalize-space(.), "Search")]""",
            },
            "address_search_button": """//a[@data-filter="search-address" and contains(normalize-space(text()), "By Address")]""",
            "street_number": """//input[contains(@class, "form-control") and @id="StreetNumber" and @name="StreetNumber" and @type="text"]""",
            "street_name": """//input[contains(@class, "form-control") and @id="StreetName" and @name="StreetName" and @type="text"]""",
            "search_button": """//button[@type="button" and contains(@onclick, "AdvancedSearch") and contains(@class, "btn btn-default") and contains(normalize-space(.), "Search")]""",
        },
        "SEARCH_RESULT_TABLE_PAGE": {
            "URL_VALIDATIONS": ["Search/Result"],
            "VALIDATION_PARAMS": {
                "search_result_table": """//*[@id="resultListDiv"]/tr""",
                "search_by_owner": """//*[@id="searchType"]""",
            },
            "search_result_table": """//*[@id="resultListDiv"]/tr""",
            "search_by_owner": """//*[@id="searchType"]""",
        },
        "SEARCH_RESULT_PAGE": {
            "URL_VALIDATIONS": ["Property/View"],
            "VALIDATION_PARAMS": {
                "property_details": """//div[@class="panel-heading" and contains(.,"Property Details")]""",
                "property_values": """//div[@class="panel-heading" and contains(.,"Property Values")]""",
            },
            "PRINT_BUTTON": """//button[contains(@class, "btn") and contains(normalize-space(.), "Print") and (@data-toggle="dropdown" or not(@data-toggle))]""",
            "PRINT_SUMMARY_VIEW": """"//a[@onclick=\"onPrintClick('printSummaryView')\"]"""

        },
    }