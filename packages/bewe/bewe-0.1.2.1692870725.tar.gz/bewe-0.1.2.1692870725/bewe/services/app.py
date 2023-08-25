from bewe.services.crawler import finmind_downloader

print('Hello World!')
finmind = finmind_downloader.FinmindWrapper()
stock_df = finmind.get_tw_stock_info()


