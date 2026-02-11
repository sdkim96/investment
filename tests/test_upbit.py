from src.client import UpbitClient

upbit = UpbitClient()

accounts = upbit.v1.accounts.get()


markets = upbit.v1.market.get_all()
print(markets)
# order = upbit.v1.orders.create()
# print(order)

candles = upbit.v1.candles.get_by_days()
print(candles)