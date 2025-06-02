from courier_methods import CourierMethods
import allure
import pytest

from data import Messages
from generators import generate_first_name


class TestCreateCourier:

    @allure.title('Создание курьера')
    def test_create_courier(self, generate_login_data):
        with allure.step('Создание курьера'):
            response = CourierMethods.create_courier(generate_login_data)
        assert response.status_code == 201, f'Ожидали 201, получили {response.status_code}'
        assert response.json().get('ok') is True, f"Ожидали 'ok': True, получили {response.json()}"
        login_body = {
            "login": generate_login_data["login"],
            "password": generate_login_data["password"]
        }
        response = CourierMethods.login_courier(login_body)
        courier_id = response.json().get("id")
        allure.attach(
            str(courier_id),
            name="Courier ID",
            attachment_type=allure.attachment_type.TEXT
        )


    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self, generate_login_data):
        with allure.step('Создание курьера первый раз'):
            first_response = CourierMethods.create_courier(generate_login_data)
        assert first_response.status_code == 201, f"Первое создание: ожидали 201, получили {first_response.status_code}"
        with allure.step('Повторное создание такого же курьера'):
            second_response = CourierMethods.create_courier(generate_login_data)
        assert second_response.status_code == 409, f"Дубликат: ожидали 409, получили {second_response.status_code}"
        response_json = second_response.json()
        assert "message" in response_json, "Нет сообщения об ошибке в теле ответа"
        assert response_json['message'] == Messages.DUPLICATE_LOGIN_MESS, f"Неожиданное сообщение: {response_json}"



    @allure.title('Создание курьера без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_required_field(self, generate_login_data, missing_field):
        body = generate_login_data.copy()
        body.pop(missing_field)
        with allure.step(f'Проверка создания курьера без поля: {missing_field}'):
            response = CourierMethods.create_courier(body)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json().get("message") == Messages.NOT_ENOUGH_DATA, \
            f"Unexpected message: {response.json()}"

    @allure.title('Нельзя создать двух курьеров с одинаковым логином')
    def test_create_courier_with_existing_login(self, generate_login_data):
        with allure.step('Создание курьера первый раз'):
            response_1 = CourierMethods.create_courier(generate_login_data)
        assert response_1.status_code == 201
        assert response_1.json().get('ok') is True
        first_name = generate_first_name()
        duplicate_data = {
            "login": generate_login_data["login"],
            "password": generate_login_data["password"],
            "firstName": first_name
        }
        with allure.step('Повторное создание курьера с таким же логином, но с другим именем'):
            response_2 = CourierMethods.create_courier(duplicate_data)

        assert response_2.status_code == 409, f"Дубликат: ожидали 409, получили {response_2.status_code}"
        assert "message" in response_2.json()
        assert response_2.json()["message"] == Messages.DUPLICATE_LOGIN_MESS, f"Неожиданное сообщение: {response_2.json()}"