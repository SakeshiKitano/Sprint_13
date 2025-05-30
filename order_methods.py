import requests

from data import Url


class OrderMethods:

    @staticmethod
    def create_order(order_body):
        response = requests.post(f'{Url.BASE_URL}{Url.ORDER_URL}/',  json=order_body)
        return response

    @staticmethod
    def get_order_list():
        response = requests.get(f'{Url.BASE_URL}{Url.ORDER_URL}/')
        return response


