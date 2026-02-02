from src.upbit.client import UpbitClient

upbit = UpbitClient()

accounts = upbit.v1.accounts.get()
print(accounts)

order = upbit.v1.orders.create()
print(order)