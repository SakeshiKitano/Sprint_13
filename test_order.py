import pytest
import allure
from order_methods import OrderMethods

class TestOrder:

    @allure.title("Создание заказа с разными цветами и без")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, order_body, colors):
        order_data = order_body
        order_data["color"] = colors

        with allure.step(f"Создание заказа с цветами: {colors}"):
            response = OrderMethods.create_order(order_data)

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert "track" in response.json(), f"No 'track' in response: {response.json()}"

    @allure.title("Проверка получения списка заказов")
    def test_get_order_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = OrderMethods.get_order_list()

        with allure.step("Проверка статуса ответа и содержимого"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            orders = response.json().get("orders")
            assert isinstance(orders, list), f"Expected list, got {type(orders)}"
