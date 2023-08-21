import dataclasses
import pandas as pd
from typing import Any, Mapping, Optional, Sequence


@dataclasses.dataclass(frozen=True)
class DataFormat:
    required_field: Sequence[str]


@dataclasses.dataclass
class DataUnit:
    format: DataFormat
    data: Mapping[Any, Any]
    actionable_price: float


class DataContainer:
    name = 'BaseContainer'

    def __init__(self, asset_name: str, data: Optional[Sequence[DataUnit]] = None):
        self.asset_name = asset_name
        self.data: Optional[Sequence[DataUnit]] = data
        self.index = 0
        self.size = 0 if not self.data else len(self.data)

    def __iter__(self) -> 'DataContainer':
        return self

    def __next__(self) -> DataUnit:
        if self.index == self.size:
            raise StopIteration

        if not self.data:
            raise StopIteration

        unit = self.data[self.index]
        self.index += 1
        return unit

    def __len__(self):
        return 0 if not self.data else len(self.data)
    
    def transform(self, data: pd.DataFrame):
        raise NotImplementedError
    
    def get_format(self) -> DataFormat:
        raise NotImplementedError
