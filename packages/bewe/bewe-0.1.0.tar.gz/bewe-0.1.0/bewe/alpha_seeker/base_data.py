import dataclasses
from typing import Any, Sequence


@dataclasses.dataclass
class DataFormat:
    window_size: int
    required_field: Sequence[str]


@dataclasses.dataclass
class DataUnit:
    format: DataFormat
    data: Sequence[Any]


class DataContainer:
    name = 'BaseContainer'

    def __init__(self, asset_name: str):
        self.asset_name = asset_name

    def __iter__(self) -> DataUnit:
        raise NotImplementedError
    
    def transform(self, data: Any):
        raise NotImplementedError
    
    def get_format(self) -> DataFormat:
        raise NotImplementedError
    
