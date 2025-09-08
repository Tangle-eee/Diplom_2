import random
import string
import requests
from datetime import datetime, timezone

from data import *


def generate_random_string(length: int) -> str:
    """Простая строка из a-z длиной length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def build_user_payload(email: str, password: str, name: str) -> dict:
    """Собрать тело запроса создания пользователя."""
    return {"email": email, "password": password, "name": name}


def generate_valid_unique_email() -> str:
    """Сделать уникальный валидный e-mail на основе времени."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"test_{ts}@example.com"


def generate_invalid_unique_email() -> str:
    """Невалидный e-mail (без символа @)."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"invalid_{ts}.example.com"



def register_user(user_data: dict) -> requests.Response:
    """POST /api/auth/register"""
    url = BASE_URL + URL_CREATE_USER
    return requests.post(url, json=user_data)


def login_user(user_data: dict) -> requests.Response:
    """POST /api/auth/login"""
    url = BASE_URL + URL_LOGIN_USER
    return requests.post(url, json={"email": user_data["email"], "password": user_data["password"]})


def get_token_and_user(user_data: dict) -> str:
    """
    Зарегистрировать (если уже есть — допустим 403) и залогиниться.
    Вернуть accessToken (в этом API он уже с префиксом 'Bearer ').
    """
    reg_res = register_user(user_data)
    assert reg_res.status_code in (200, 201, 403), f"register failed: {reg_res.status_code} {reg_res.text}"

    login_res = login_user(user_data)
    assert login_res.status_code == 200, f"login failed: {login_res.status_code} {login_res.text}"

    token = login_res.json().get("accessToken")
    assert token, "no accessToken in login response"
    return token


def delete_user(access_token: str) -> requests.Response | None:
    """DELETE /api/auth/user — удалить пользователя по токену."""
    if not access_token:
        return None
    url = BASE_URL + URL_USER
    headers = {"Authorization": access_token}  # токен уже содержит 'Bearer '
    return requests.delete(url, headers=headers)


def get_ingredients() -> list[str]:
    """Вернуть несколько валидных _id ингредиентов для заказов."""
    url = BASE_URL + URL_INGRIDIENTS
    res = requests.get(url)
    assert res.status_code == 200, f"ingredients failed: {res.status_code} {res.text}"
    data = res.json().get("data", [])
    assert data, "ingredients list is empty"
    return [i["_id"] for i in data[:3]]  # берём первые 2-3 id
