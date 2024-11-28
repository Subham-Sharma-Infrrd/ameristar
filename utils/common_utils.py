from collections import defaultdict
import re
import uuid
from fuzzywuzzy import fuzz
import usaddress
from log import logger


def generate_unique_id():
    """
    Generates a unique identifier.

    Returns:
        str: A unique ID as a string.
    """
    # Generate a unique ID (UUID4 is random-based)
    unique_id = str(uuid.uuid4())
    logger.info(f"Generated Unique ID: {unique_id}")
    return unique_id

def is_fuzzy_match(header_text, expected_headers, threshold=80):
    for expected in expected_headers:
        score = fuzz.ratio(header_text.strip().lower(), expected.strip().lower())
        if score >= threshold:
            return True
    return False

def name_and_address_parser(address_text: str):
    """
    Will parse the USA address into street, city, state, and zipcode
    :param address_text: valid address
    :return: Object of Address class
    """

    match = re.search(r" \d{3,4}[\d -]{4,10}", address_text)
    zip_ = ""
    if match:
        zip_ = match.group()

    parse_address = usaddress.parse(address_text)
    address_dict = defaultdict(list)
    split_address_dict = defaultdict(list)
    remove_tags = []
    for t in parse_address:
        address_dict[t[1]].append(t[0])
        if t[1] in [
            "Recipient",
            "PlaceName",
            "StateName",
            "ZipCode",
            "CountryName",
        ]:
            remove_tags.append(t)

    parse_address = [t for t in parse_address if t not in remove_tags]  
    split_address_dict["city"] = " ".join(address_dict.pop("PlaceName", []))
    split_address_dict["state_name"] = " ".join(address_dict.pop("StateName", []))
    split_address_dict["zip_code"] = " ".join(address_dict.pop("ZipCode", [])) if not zip_ else zip_
    # country not being used currently
    split_address_dict["country"] = " ".join(address_dict.pop("CountryName", []))
    split_address_dict["street_address"] = " ".join([t[0] for t in parse_address if t[0] not in zip_])
    return split_address_dict 
