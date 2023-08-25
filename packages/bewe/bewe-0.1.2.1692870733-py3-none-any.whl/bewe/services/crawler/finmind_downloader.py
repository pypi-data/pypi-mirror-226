import requests
from bewe.services.crawler import secret_manager
from bewe.services.databases import asset_orm
from bewe.services.databases import db_manager
from FinMind.data import data_loader

_FINMIND_KEY = 'FINMIND_API'


class FinmindWrapper:
    def __init__(self):
        self.token = secret_manager.get_secret_tokens(_FINMIND_KEY)
        self.data_loader = data_loader.DataLoader()
        self.data_loader.login_by_token(self.token)
        self.db_manager = db_manager.DBManager()

    def get_tw_stock_info(self):
        df = self.data_loader.taiwan_stock_info()

        stocks, categories = [], []
        for _, row in df.iterrows():
            stock = asset_orm.Stock(
                stock_id=row.stock_id,
                stock_name=row.stock_name
            )

            category = asset_orm.Category(
                stock_id=row.stock_id,
                category=row.industry_category
            )

            stocks.append(stock)
            categories.append(category)

        self.db_manager.update(stocks)
        self.db_manager.update(categories)


