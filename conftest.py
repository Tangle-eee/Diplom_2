import pytest
from helpers import (
    generate_valid_unique_email,
    generate_random_string,
    build_user_payload,
    get_token_and_user,
    delete_user,
    get_ingredients,
)


@pytest.fixture
def unique_valid_email():
    return generate_valid_unique_email()


@pytest.fixture
def user_data(unique_valid_email):
    """Собираем валидные данные пользователя."""
    email = unique_valid_email
    password = generate_random_string(10)
    name = generate_random_string(10)
    return build_user_payload(email, password, name)


@pytest.fixture
def token(user_data):
    """
    Создаём пользователя и логинимся, отдаём accessToken.
    После теста — удаляем пользователя.
    """
    t = get_token_and_user(user_data)
    yield t
    delete_user(t)


@pytest.fixture
def ingredient_ids():
    """Список валидных id ингредиентов (2-3 штуки)."""
    return get_ingredients()
