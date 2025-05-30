from courier_methods import CourierMethods
import allure
import pytest
from faker import Faker
fake = Faker()

class TestCreateCourier:

    @allure.title('Создание курьера')
    def test_create_courier(self, generate_login_data):
        with allure.step('Создание курьера'):
            response = CourierMethods.create_courier(generate_login_data)
        assert response.status_code == 201, f'Ожидали 201, получили {response.status_code}'
        assert response.json().get('ok') is True, f"Ожидали 'ok': True, получили {response.json()}"

        login_resp = CourierMethods.login_courier({
            "login": generate_login_data["login"],
            "password": generate_login_data["password"]
        })
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                CourierMethods.delete_courier(courier_id)

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
        assert response_json['message'] == "Этот логин уже используется. Попробуйте другой.", f"Неожиданное сообщение: {response_json}"

        login_resp = CourierMethods.login_courier({
            "login": generate_login_data["login"],
            "password": generate_login_data["password"]
        })
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                CourierMethods.delete_courier(courier_id)

    @allure.title('Создание курьера без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_required_field(self, generate_login_data, missing_field):
        body = generate_login_data.copy()
        body.pop(missing_field)
        with allure.step(f'Проверка создания курьера без поля: {missing_field}'):
            response = CourierMethods.create_courier(body)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи", \
            f"Unexpected message: {response.json()}"

    @allure.title('Нельзя создать двух курьеров с одинаковым логином')
    def test_create_courier_with_existing_login(self, generate_login_data):
        with allure.step('Создание курьера первый раз'):
            response_1 = CourierMethods.create_courier(generate_login_data)
        assert response_1.status_code == 201
        assert response_1.json().get('ok') is True

        duplicate_data = {
            "login": generate_login_data["login"],
            "password": generate_login_data["password"],
            "firstName": fake.first_name()
        }
        with allure.step('Повторное создание курьера с таким же логином, но с другим именем'):
            response_2 = CourierMethods.create_courier(duplicate_data)

        assert response_2.status_code == 409, f"Дубликат: ожидали 409, получили {response_2.status_code}"
        assert "message" in response_2.json()
        assert response_2.json()["message"] == "Этот логин уже используется. Попробуйте другой.", f"Неожиданное сообщение: {response_2.json()}"