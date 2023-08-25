import datetime
import sqlalchemy
from bewe.services.databases import db_manager
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    stock_name = sqlalchemy.Column(sqlalchemy.String(60))
    flag = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    last_execution = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, stock_id, stock_name):
        self.stock_id = stock_id
        self.stock_name = stock_name


class Category(Base):
    __tablename__ = 'stock_category'

    stock_id = sqlalchemy.Column(
        sqlalchemy.String(50), sqlalchemy.ForeignKey('stock.stock_id'), nullable=False, primary_key=True)
    category = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, stock_id, category):
        self.stock_id = stock_id
        self.category = category


class StockPrice(Base):
    __tablename__ = 'stock_price'

    stock_id = sqlalchemy.Column(
        sqlalchemy.String(50), sqlalchemy.ForeignKey('stock.stock_id'), nullable=False, primary_key=True)
    open_price = sqlalchemy.Column(sqlalchemy.Float(8))
    close_price = sqlalchemy.Column(sqlalchemy.Float(8))
    max_price = sqlalchemy.Column(sqlalchemy.Float(8))
    min_price = sqlalchemy.Column(sqlalchemy.Float(8))
    volume = sqlalchemy.Column(sqlalchemy.Float(8))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


def create_delete_all():
    db = db_manager.DBManager()
    engine = db.engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_delete_all()

