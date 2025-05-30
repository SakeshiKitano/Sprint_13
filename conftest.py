import pytest
from data import DataForOrder
from courier_methods import CourierMethods


from generators import register_new_courier_and_return_login_password, generate_courier_creds

@pytest.fixture
def generate_login_data():
    creds = generate_courier_creds()
    body = {
        "login": creds[0],
        "password": creds[1],
        "firstName": creds[2]
    }
    yield body

@pytest.fixture
def registered_courier(generate_login_data):
    response = CourierMethods.create_courier(generate_login_data)
    assert response.status_code == 201, "Failed to create courier in fixture"
    login_body = {
        "login": generate_login_data["login"],
        "password": generate_login_data["password"]
    }
    yield login_body
    login_resp = CourierMethods.login_courier(login_body)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        if courier_id:
            CourierMethods.delete_courier(courier_id)


@pytest.fixture
def order_body():
    body = DataForOrder.CREATE_ORDER.copy()
    yield body








