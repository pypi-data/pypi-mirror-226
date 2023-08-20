from bewe.alpha_seeker import base_strategy
from bewe.alpha_seeker import base_data
import holder


class BackTester:
    def __init__(self, bank: holder.Bank):
        self.bank = bank

    def backtest(self, strategy: base_strategy.Strategy, data: base_data.DataContainer):
        pass
