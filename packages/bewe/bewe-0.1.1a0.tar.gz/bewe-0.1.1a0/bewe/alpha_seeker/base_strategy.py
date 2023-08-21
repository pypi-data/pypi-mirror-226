import dataclasses
import enum
from bewe.alpha_seeker import base_data
from typing import Optional


class Action(enum.Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


@dataclasses.dataclass
class Execution:
    action: Action
    confidence: Optional[float] = None
    gain: Optional[float] = None


class Strategy:
    strategy_name = 'Base Strategy'

    def predict(self, data: base_data.DataUnit) -> Execution:
        raise NotImplementedError
    
    def validate_data(self, data: base_data.DataUnit) -> bool:
        raise NotImplementedError

