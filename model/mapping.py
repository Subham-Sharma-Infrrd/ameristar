from dataclasses import dataclass, field
from typing import Any, List, Optional, TypedDict
from model import camelcase


@dataclass
class MappingRequest:
    address : str
    city: str
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

    def to_json(self):
        return dict(requestId=self.requestId, status=self.status, documents=self.documents)
