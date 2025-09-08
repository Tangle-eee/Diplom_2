import requests
import allure
import pytest

from data import BASE_URL, URL_CREATE_USER, URL_LOGIN_USER, URL_USER


@allure.epic("Создание пользователя")
@allure.feature("Создание пользователя")
class TestRegisterUser:
    url_reg = BASE_URL + URL_CREATE_USER

    @allure.title("Успешное создание уникального пользователя")
    def test_register_unique_user(self, user_data):
        res = requests.post(self.url_reg, json=user_data)
        assert res.status_code in (200, 201)
        body = res.json()
        assert body.get("success") is True
        assert "accessToken" in body

        # удаляем созданного пользователя
        token = body["accessToken"]
        requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_register_existing_user(self, user_data):
        # создаём
        first = requests.post(self.url_reg, json=user_data)
        assert first.status_code in (200, 201)
        token = first.json().get("accessToken")

        try:
            # пытаемся создать повторно
            res = requests.post(self.url_reg, json=user_data)
            assert res.status_code in (403, 409)
            assert res.json().get("success") is False
        finally:
            # чистим
            if token:
                requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

    @allure.title("Создание пользователя с пропущенным обязательным полем")
    @pytest.mark.parametrize("missing", ["email", "password", "name"])
    def test_register_missing_required_field(self, user_data, missing):
        bad = dict(user_data)
        bad.pop(missing)
        res = requests.post(self.url_reg, json=bad)
        assert res.status_code in (400, 403)
        assert res.json().get("success") is False


@allure.epic("Логин пользователя")
@allure.feature("Логин")
class TestLoginUser:
    url_login = BASE_URL + URL_LOGIN_USER
    url_reg = BASE_URL + URL_CREATE_USER

    @allure.title("Логин под существующим пользователем")
    def test_login_ok(self, user_data):
        # регистрируем
        reg = requests.post(self.url_reg, json=user_data)
        assert reg.status_code in (200, 201)
        token = reg.json().get("accessToken")

        try:
            # логинимся
            res = requests.post(self.url_login, json={"email": user_data["email"], "password": user_data["password"]})
            assert res.status_code == 200
            assert res.json().get("success") is True
            assert "accessToken" in res.json()
        finally:
            if token:
                requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

    @allure.title("Логин с неверными логином/паролем")
    def test_login_wrong_creds(self):
        res = requests.post(self.url_login, json={"email": "wrong@example.com", "password": "badpass"})
        assert res.status_code in (401, 403)
        assert res.json().get("success") is False


@allure.epic("Изменение данных пользователя")
@allure.feature("PATCH /api/auth/user")
class TestPatchUser:
    url_user = BASE_URL + URL_USER
    url_reg = BASE_URL + URL_CREATE_USER

    @allure.title("Изменение данных с авторизацией — можно менять любые поля")
    @pytest.mark.parametrize("field,new_value", [
        ("name", "ChangedName"),
        ("email", "changed@example.com"),
        ("password", "NewP@ssw0rd!"),
    ])
    def test_patch_authorized(self, user_data, field, new_value):
        # регистрируем и берём токен
        reg = requests.post(self.url_reg, json=user_data)
        assert reg.status_code in (200, 201)
        token = reg.json().get("accessToken")

        try:
            res = requests.patch(self.url_user, headers={"Authorization": token}, json={field: new_value})
            assert res.status_code == 200
            assert res.json().get("success") is True
        finally:
            if token:
                requests.delete(self.url_user, headers={"Authorization": token})

    @allure.title("Изменение данных без авторизации — ошибка")
    @pytest.mark.parametrize("field,new_value", [
        ("name", "AnonName"),
        ("email", "anon@example.com"),
        ("password", "AnonPass123"),
    ])
    def test_patch_unauthorized(self, field, new_value):
        res = requests.patch(self.url_user, json={field: new_value})
        assert res.status_code in (401, 403)
        body = res.json()
        assert body.get("success") is False
        # если в проекте проверяют текст ошибки:
        # assert "You should be authorised" in body.get("message", "")
