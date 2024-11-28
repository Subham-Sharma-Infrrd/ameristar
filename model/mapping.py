"""
Web_scrapping object definitions
"""
from enum import Enum


from dataclasses import dataclass, field



class WebScrappingDocType(Enum):
    CAD = "CAD"
    TAX = "TAX"

class WebScrappingWebPageTypes(Enum):
    HOMEPAGE = "HOMEPAGE"
    SEARCH_RESULT_TABLE_PAGE = "SEARCH_RESULT_TABLE_PAGE"
    SEARCH_RESULT_PAGE = "SEARCH_RESULT_PAGE"


class WebSurfMode(Enum):
    STEALTH= "STEALTH"
    NORMAL = "NORMAL"


@dataclass
class MappingRequest:
    street_number : str
    street_address : str
    # city: str
    state : str
    county : str
    owner_name : str
    job_id : int
    order_id : int

    def to_json(self):
        return dict(requestId=self.requestId, status=self.status, documents=self.documents)


@dataclass
class MappingResponse:
    cad : str
    tax: str
    job_id : int
    order_id : int
    account_number: str
    unique_id: str

    def to_json(self):
        return dict(requestId=self.requestId, status=self.status, documents=self.documents)

