import requests
import json


class APIException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Не удалось обработать количество валюты.")

        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")

        base = base.upper()
        quote = quote.upper()

        available_currencies = ['USD', 'EUR', 'RUB']
        if base not in available_currencies:
            raise APIException(f"Валюта '{base}' не найдена. Доступные валюты: {', '.join(available_currencies)}")
        if quote not in available_currencies:
            raise APIException(f"Валюта '{quote}' не найдена. Доступные валюты: {', '.join(available_currencies)}")

        try:
            url = f"https://v6.exchangerate-api.com/v6/c2731c58b0bdd53dfe9adab9/latest/{base}"
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.content)
            rate = data['conversion_rates'][quote]
            price = rate * amount
        except requests.exceptions.RequestException:
            raise APIException('Ошибка подключения к API обмена валют.')
        except (KeyError, ValueError):
            raise APIException('Не удалось получить курс валюты.')

        return price

