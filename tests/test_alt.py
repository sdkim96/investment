from src.client import AlternativeClient


client = AlternativeClient()

fng_data = client.fng.get()
print(fng_data)