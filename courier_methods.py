import requests

from data import Url


class CourierMethods:
    @staticmethod
    def create_courier(body):
        return requests.post(f'{Url.BASE_URL}{Url.CREATE_COURIER_URL}', json=body)

    @staticmethod
    def login_courier(body):
        return requests.post(f'{Url.BASE_URL}{Url.LOGIN_COURIER_URL}', json=body)

    @staticmethod
    def delete_courier(courier_id):
        return requests.delete(f'{Url.BASE_URL}{Url.CREATE_COURIER_URL}/{courier_id}')


