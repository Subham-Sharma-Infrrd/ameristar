"""
field dictionary collection DBO
"""

from dataclasses import asdict, dataclass, field
from typing import Set


@dataclass
class FieldDictionary:
    """
    DBO for field_dictionary collection
    """

    _id: str = field(default="", metadata={"allow_none": True})
    fieldId: str = field(default="", metadata={"allow_none": True})
    userModelId: str = field(default="", metadata={"allow_none": True})
    values: Set = field(default_factory=set, metadata={"allow_none": True})
    keys: list = field(default_factory=list, metadata={"allow_none": True})

    def to_dict(self):
        """Converts a field_dictionary obj into a dict"""
        return asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
