from courier_methods import CourierMethods
import allure
import pytest
from faker import Faker
fake = Faker()

class TestLoginCourier:

    @allure.title('Логин курьера')
    def test_success_login_courier(self, registered_courier):
        with allure.step('Вход в логин курьера'):
            response = CourierMethods.login_courier(registered_courier)
        assert response.status_code == 200
        assert "id" in response.json()
        courier_id = response.json().get("id")
        print(f"Courier ID after login: {courier_id}")

    @allure.title('Авторизация без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, registered_courier, missing_field):
        login_body = registered_courier.copy()
        login_body.pop(missing_field)
        with allure.step(f'Вход в логин курьера без поля: {missing_field}'):
            response = CourierMethods.login_courier(login_body)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для входа", \
            f"Unexpected message: {response.json()}"

    @allure.title('Ошибка при неверном логине')
    def test_login_with_wrong_login(self, registered_courier):
        login_body = {
            "login": "wrong" + registered_courier["login"],
            "password": registered_courier["password"]
        }
        response = CourierMethods.login_courier(login_body)

        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title('Ошибка при неверном пароле')
    def test_login_with_wrong_password(self, registered_courier):
        login_body = {
            "login": registered_courier["login"],
            "password": "wrong" + registered_courier["password"]
        }
        response = CourierMethods.login_courier(login_body)

        assert response.status_code == 404
        assert "message" in response.json()


