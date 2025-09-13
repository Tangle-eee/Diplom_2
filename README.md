```markdown
# Diplom_2

# Тесты API Stellar Burgers

Проект содержит автотесты для проверки основных ручек API сервиса **Stellar Burgers**.

## Стек
- [pytest](https://docs.pytest.org/)
- [requests](https://docs.python-requests.org/)
- [allure-pytest](https://docs.qameta.io/allure/)

## Что покрыто тестами

### Пользователи
- Регистрация:
  - создание уникального пользователя
  - создание пользователя, который уже зарегистрирован
  - создание без одного из обязательных полей (email, password, name)
- Авторизация:
  - успешный логин
  - логин с неверными данными
- Изменение данных:
  - с авторизацией (имя, email, пароль)
  - без авторизации (ошибка)

### Заказы
- Создание заказа:
  - с авторизацией и ингредиентами
  - без авторизации
  - без ингредиентов (ошибка)
  - с неверным id ингредиента (ошибка)
- Получение заказов:
  - авторизованного пользователя
  - без авторизации (ошибка)

## Структура проекта
```

.
├── data.py              # Константы API
├── helpers.py           # Утилиты для работы с API
├── conftest.py          # Фикстуры pytest
├── tests/               # Тесты по эндпоинтам
│   ├── test\_user.py
│   └── test\_order.py
├── requirements.txt
├── pytest.ini           # Конфигурация pytest (allure)
└── README.md

````

## Конфигурация pytest

Файл **pytest.ini**:
```ini
[pytest]
addopts = -q --alluredir=allure-results
````

Это позволяет автоматически сохранять результаты тестов для Allure в папку `allure-results`.

## Запуск тестов

1. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Запустить тесты:

   ```bash
   pytest
   ```

3. Сгенерировать и просмотреть отчёт Allure:

   ```bash
   allure serve allure-results
   ```
