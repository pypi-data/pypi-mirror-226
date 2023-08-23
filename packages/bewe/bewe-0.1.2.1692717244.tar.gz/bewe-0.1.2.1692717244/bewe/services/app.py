from bewe.services.crawler import db_manager

print('Hello World!')
manager = db_manager.DBManager()
result = manager.execute_query('SELECT * FROM asset.stock')

for res in result:
    print('Res:', res)

