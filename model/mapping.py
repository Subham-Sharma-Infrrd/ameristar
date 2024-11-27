from dataclasses import dataclass, field
from typing import Any, List, Optional, TypedDict
from model import camelcase


@dataclass
class MappingRequest:
    address : str
    city: str
    state : str
    county : str
    ownerName : str
    jobId : int
    orderId : int

    def to_json(self):
        return dict(requestId=self.requestId, status=self.status, documents=self.documents)


@dataclass
class MappingResponse:
    cad : str
    tax: str
    jobId : int
    orderId : int

    def to_json(self):
        return dict(cad=self.cad, tax=self.tax, jobId=self.jobId, orderId=self.orderId)
