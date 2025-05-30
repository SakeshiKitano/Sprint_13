class Url:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'
    CREATE_COURIER_URL = '/api/v1/courier'
    LOGIN_COURIER_URL = '/api/v1/courier/login'
    ORDER_URL = '/api/v1/orders'


class DataForOrder:
    CREATE_ORDER = {
    "firstName": "Test",
    "lastName": "User",
    "address": "Test street",
    "metroStation": 4,
    "phone": "+7 999 999 99 99",
    "rentTime": 2,
    "deliveryDate": "2025-06-01",
    "comment": "Test order",
    "color": []
}