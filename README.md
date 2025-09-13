```markdown
# Дипломный проект. Задание 2 — API-тесты

Набор автотестов для проверки REST API сервиса **Stellar Burgers** с использованием `pytest`, `requests` и `allure`.

## Структура проекта

```

.
├── data.py              # Константы API (базовый URL и эндпоинты)
├── helpers.py           # Утилиты для работы с API
├── conftest.py          # фикстуры pytest (пользователи, токены, ингредиенты)
├── tests/               # тесты по эндпоинтам
│   ├── test\_user.py     # регистрация, логин, изменение данных пользователя
│   └── test\_order.py    # создание заказов и получение истории заказов
├── requirements.txt     # зависимости
├── pytest.ini           # базовые опции pytest + allure
└── README.md

````

## Требования

* Python 3.10+
* `pip` для установки зависимостей
* [Allure](https://docs.qameta.io/allure/) для просмотра отчётов

## Установка

```bash
pip install -r requirements.txt
````

## Как устроен `pytest.ini`

Файл `pytest.ini` задаёт дефолтные опции:

* `addopts = -q --alluredir=allure-results` — при каждом запуске `pytest`:

  * тесты выполняются в «тихом» режиме (`-q`);
  * результаты сохраняются в директорию `allure-results/` для последующего формирования отчёта.

## Запуск тестов

Запусти:

```bash
pytest
```

## Просмотр отчёта Allure

Чтобы сгенерировать и открыть красивый HTML-отчёт:

```bash
allure serve allure-results
```
