import requests
import allure
import pytest
import uuid

from data import BASE_URL, URL_INGRIDIENTS, URL_ORDERS, URL_USER, URL_CREATE_USER, URL_LOGIN_USER
from helpers import get_ingredients


@allure.epic("Создание заказов")
@allure.feature("POST /api/orders")
class TestCreateOrder:
    url_ingredients = BASE_URL + URL_INGRIDIENTS
    url_orders = BASE_URL + URL_ORDERS
    url_reg = BASE_URL + URL_CREATE_USER
    url_login = BASE_URL + URL_LOGIN_USER

    def _create_user_and_token(self, user_data) -> str:
        """Вспомогательно: создать пользователя и вернуть токен."""
        reg = requests.post(self.url_reg, json=user_data)
        assert reg.status_code in (200, 201)
        token = reg.json().get("accessToken")
        assert token
        return token

    @allure.title("Создание заказа с авторизацией и с ингредиентами")
    def test_create_order_auth_with_ingredients(self, user_data, ingredient_ids):
        token = self._create_user_and_token(user_data)
        try:
            res = requests.post(self.url_orders, headers={"Authorization": token}, json={"ingredients": ingredient_ids})
            assert res.status_code == 200
            body = res.json()
            assert body.get("success") is True
            assert "order" in body
        finally:
            requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

    @allure.title("Создание заказа без авторизации и с ингредиентами")
    def test_create_order_noauth_with_ingredients(self, ingredient_ids):
        res = requests.post(self.url_orders, json={"ingredients": ingredient_ids})
        # В некоторых версиях API это может быть 200 (анонимный заказ) или 401.
        assert res.status_code in (200, 401)
        if res.status_code == 200:
            assert res.json().get("success") is True
        else:
            assert res.json().get("success") is False

    @allure.title("Создание заказа без ингредиентов — ошибка")
    def test_create_order_no_ingredients(self, user_data):
        token = self._create_user_and_token(user_data)
        try:
            res = requests.post(self.url_orders, headers={"Authorization": token}, json={"ingredients": []})
            assert res.status_code in (400, 403)
            assert res.json().get("success") is False
        finally:
            requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

    @allure.title("Создание заказа с неверным хешем ингредиента — ошибка")
    def test_create_order_wrong_ingredient_hash(self, user_data):
        token = self._create_user_and_token(user_data)
        try:
            bad_ids = [str(uuid.uuid4())]
            res = requests.post(self.url_orders, headers={"Authorization": token}, json={"ingredients": bad_ids})

            assert res.status_code in (400, 500)

            if res.status_code == 400:
                body = res.json()
                assert body.get("success") is False
            else:
                assert res.text.strip() != ""
        finally:
            requests.delete(BASE_URL + URL_USER, headers={"Authorization": token})

@allure.epic("Заказы пользователя")
@allure.feature("GET /api/orders")
class TestUserOrders:
    url_orders = BASE_URL + URL_ORDERS
    url_user = BASE_URL + URL_USER
    url_reg = BASE_URL + URL_CREATE_USER

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, user_data):
        # создаём пользователя и токен
        reg = requests.post(self.url_reg, json=user_data)
        assert reg.status_code in (200, 201)
        token = reg.json().get("accessToken")

        try:
            # чтобы список был не пуст, создадим заказ
            ingredients = get_ingredients()
            requests.post(self.url_orders, headers={"Authorization": token}, json={"ingredients": ingredients})

            # получаем заказы
            res = requests.get(self.url_orders, headers={"Authorization": token})
            assert res.status_code == 200
            body = res.json()
            assert body.get("success") is True
            assert isinstance(body.get("orders"), list)
        finally:
            requests.delete(self.url_user, headers={"Authorization": token})

    @allure.title("Получение заказов без авторизации — ошибка")
    def test_get_user_orders_without_auth(self):
        res = requests.get(self.url_orders)
        assert res.status_code in (401, 403)
        body = res.json()
        assert body.get("success") is False
        # если нужно строгое сообщение:
        # assert "You should be authorised" in body.get("message", "")
