from fuzzywuzzy import fuzz


def is_fuzzy_match(header_text, expected_headers, threshold=80):
    for expected in expected_headers:
        score = fuzz.ratio(header_text.strip().lower(), expected.strip().lower())
        if score >= threshold:
            return True
    return False