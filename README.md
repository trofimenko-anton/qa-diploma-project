# qa-diploma-project

Дипломный проект QA-инженера по ручному и автоматизированному тестированию веб-приложения **YouGile**.

В проекте реализованы автоматизированные тесты для веб-интерфейса и REST API с использованием **Python, Pytest, Selenium, Requests и Allure Report**.

## Содержание

* [Описание проекта](#описание-проекта)
* [Технологии](#технологии)
* [Что тестируется](#что-тестируется)
* [Структура проекта](#структура-проекта)
* [Установка и настройка](#установка-и-настройка)
* [Конфигурация `.env`](#конфигурация-env)
* [Запуск тестов](#запуск-тестов)
* [Allure Report](#allure-report)

## Описание проекта

Проект предназначен для автоматизации тестирования веб-приложения [YouGile](https://ru.yougile.com) и его **REST API v2**.

Автоматизация выполнена на языке **Python** с использованием библиотеки **pytest**.

Для UI-тестирования используется **Selenium** и паттерн **Page Object**.

Для API-тестирования используется библиотека **Requests**.

Для формирования подробных отчётов о результатах тестирования используется **Allure Report**.

## Технологии

Основные инструменты и технологии проекта:

* Python
* Pytest
* Selenium
* Requests
* Allure Report
* Page Object
* `.env` для хранения конфигурации
* Git / GitHub
* Visual Studio Code

## Что тестируется

Автоматизированные тесты покрывают основные пользовательские и API-сценарии YouGile.

### UI-тесты

Проверяются:

* авторизация пользователя;
* создание проекта;
* создание и управление задачами;
* просмотр и редактирование задач;
* поиск задач.

### API-тесты

Проверяется работа REST API YouGile v2, включая:

* получение данных пользователя;
* создание проекта;
* создание доски;
* создание колонки;
* создание задачи;
* получение задачи;
* обновление задачи;
* негативные сценарии.

## Структура проекта

```text
qa-diploma-project/
│
├── yougile-tests/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── boards_page.py
│   │   └── tasks_page.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_api.py
│       └── test_ui.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

### Назначение основных файлов

`config/` — конфигурация проекта и настройки тестового окружения.

`pages/` — Page Object модели страниц веб-приложения.

`tests/` — автоматизированные тесты.

`conftest.py` — фикстуры pytest, используемые тестами.

`test_ui.py` — UI-тесты Selenium.

`test_api.py` — API-тесты Requests.

`.env.example` — пример файла с переменными окружения.

`pytest.ini` — конфигурация pytest и зарегистрированные маркеры тестов.

`requirements.txt` — зависимости Python.

## Установка и настройка

### 1. Клонирование репозитория

Клонируйте репозиторий проекта:

```powershell
git clone <URL_репозитория>
cd qa-diploma-project
```

### 2. Создание виртуального окружения

Создайте виртуальное окружение:

```powershell
python -m venv venv
```

Активируйте виртуальное окружение:

```powershell
.\venv\Scripts\Activate.ps1
```

После активации в терминале должно отображаться имя виртуального окружения `venv`.

### 3. Установка зависимостей

Установите все необходимые зависимости:

```powershell
pip install -r requirements.txt
```

### 4. Создание файла `.env`

Создайте файл `.env` на основе шаблона `.env.example`:

```powershell
Copy-Item .env.example .env
```

После этого откройте файл `.env` и укажите собственные значения переменных.

## Конфигурация `.env`

Пример содержимого файла:

```env
BASE_URL=https://ru.yougile.com
YOUGILE_LOGIN=your_email@example.com
YOUGILE_PASSWORD=your_password
YOUGILE_TOKEN=your_api_token
BROWSER=chrome
```

### Назначение переменных

| Переменная         | Назначение                 |
| ------------------ | -------------------------- |
| `BASE_URL`         | URL веб-приложения YouGile |
| `YOUGILE_LOGIN`    | Логин пользователя         |
| `YOUGILE_PASSWORD` | Пароль пользователя        |
| `YOUGILE_TOKEN`    | API-токен YouGile          |
| `BROWSER`          | Браузер для UI-тестов      |

> **Важно:** файл `.env` содержит конфиденциальные данные и не должен добавляться в Git-репозиторий. Для публикации используется файл `.env.example`.

## Запуск тестов

Все команды запускаются из папки `yougile-tests`.

Перейдите в папку с тестами:

```powershell
cd yougile-tests
```

### Запуск всех тестов

```powershell
pytest -v
```

### Запуск только UI-тестов

```powershell
pytest -m "ui" -v
```

### Запуск только API-тестов

```powershell
pytest -m "api" -v
```

### Запуск конкретного файла с тестами

UI-тесты:

```powershell
pytest tests/test_ui.py -v
```

API-тесты:

```powershell
pytest tests/test_api.py -v
```

## Allure Report

Для формирования отчёта Allure сначала необходимо выполнить тесты с сохранением результатов:

```powershell
pytest --alluredir=allure-results
```

После завершения тестов запустите Allure:

```powershell
allure serve allure-results
```

После запуска команда автоматически создаёт локальный отчёт и открывает его в браузере.

### Результаты Allure

В отчёте отображаются:

* список выполненных тестов;
* статус каждого теста;
* названия тестов;
* шаги выполнения;
* параметры;
* описание ошибок;
* дополнительная информация о выполнении тестов.

## Рекомендуемый порядок запуска

Для полного запуска проекта рекомендуется использовать следующий порядок:

```text
1. Клонировать репозиторий
        ↓
2. Перейти в папку qa-diploma-project
        ↓
3. Создать и активировать venv
        ↓
4. Установить зависимости
        ↓
5. Создать и заполнить .env
        ↓
6. Перейти в папку yougile-tests
        ↓
7. Запустить pytest
        ↓
8. При необходимости сформировать Allure Report
```

### Полный пример запуска в PowerShell

```powershell
git clone <URL_репозитория>
cd qa-diploma-project

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env
```

После заполнения `.env`:

```powershell
cd yougile-tests

pytest -v
```

Для формирования Allure Report:

```powershell
pytest --alluredir=allure-results
allure serve allure-results
```

## Результат

В результате выполнения тестов проверяется работоспособность основных функций веб-приложения YouGile и его REST API.

Все автоматизированные тесты запускаются с помощью **pytest**, а результаты могут быть представлены в виде подробного **Allure Report**.
