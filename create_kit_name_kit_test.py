import requests

import data
import sender_stand_request
import configuration


def get_user_token():
    response = requests.post(
        configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
        json=data.user_body,
        headers=data.headers
    )
    return response.json()['authToken']


def get_auth_headers():
    return {
        "Authorization": f"Bearer {get_user_token()}"
    }

AUTH_HEADERS = get_auth_headers()


def get_kit_body(kit_name):
    current_body = data.kit_body.copy()
    current_body["name"] = kit_name
    return current_body


def positive_assert(kit_name):
    kit_body = get_kit_body(kit_name)
    kit_response = sender_stand_request.post_new_client_kit(kit_body, AUTH_HEADERS)
    assert kit_response.status_code == 201
    response_data = kit_response.json()
    assert response_data["name"] == kit_name


def negative_assert_code_400(kit_body):
   kit_response = sender_stand_request.post_new_client_kit(kit_body, AUTH_HEADERS)
   assert kit_response.status_code == 400


def test_create_kit_1_success_response():
    positive_assert("a")


def test_create_kit_511_success_response():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


def test_create_kit_0_symbols_success_response():
    kit_body = data.kit_body.copy()
    kit_body["name"] = ""
    negative_assert_code_400(kit_body) 


def test_create_kit_512_success_response():
    kit_body = data.kit_body.copy()
    kit_body["name"] = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabCd"
    negative_assert_code_400(kit_body)  


def test_create_kit_english_success_response():
    positive_assert("QWErty")


def test_create_kit_russian_success_response():
    positive_assert("Мария")  


def test_create_kit_special_symbols_success_response():
    positive_assert("№%@")


def test_create_kit_whitespace_success_response():
    positive_assert("Человек и КО")


def test_create_kit_number_success_response():
    positive_assert("123")


def test_create_kit_without_param_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    negative_assert_code_400(kit_body)


def test_create_kit_another_data_type_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body["name"] = 123
    negative_assert_code_400(kit_body)
