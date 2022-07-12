import requests
import json

from config import keys


class APIException(Exception):
    pass


class Cryptoconwerter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        if quote == base:
            raise APIException("Невозможно перевести одинаковые валюты")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        coste_base = (json.loads(r.content)[keys[base]]) * amount

        return coste_base
