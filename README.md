# Django-service-tree-menu

---
**Язык программирования:**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)

**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/Django-v5.1-blue?logo=Django)](https://www.djangoproject.com/)

**Базы данных:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)

**CI/CD:**

[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?logo=gunicorn)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)

---
[![Poetry](https://img.shields.io/badge/Poetry-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/poetry/)
[![Ruff](https://img.shields.io/badge/Ruff-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/ruff/)
[![pre-commit](https://img.shields.io/badge/pre_commit-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/pre_commit/)

## Описание

Django сервис: древовидное меню

## Инструкция по развёртыванию проекта

* клонировать проект на компьютер

    ```bash
    git clone https://github.com/PoBidauGustang/Django-service-tree-menu.git

    ```

* Настройки проекта заданы в .env, в .env.example для примера заданы валидные значения переменных

    ```bash
    cd Django-service-tree-menu && cp .env.example .env
    ```

* Запуск миграций для БД и сбор статики привязан к переменной DEBUG=True

Сервис реализован в контейнерах Docker

* запуск docker-compose

    ```bash
    docker compose up -d --build
    ```

* остановка docker-compose, для удаления данных (volumes) доабвтье опцию -v

    ```bash
    docker compose down
    # для удаления данных (volumes) доабвтье опцию -v
    docker compose down -v
    ```

Проект будет развернут по адресу <http://localhost>

Главная страница:

* <http://localhost/menu/>

Админка: данные для входа указываются в .env

* <http://localhost/admin/>

## Описание работы

На главной странице - <http://localhost/menu/> -представлены тестовые меню. При клике по названию меню происходит переход на его страницу, а возврат обратно осуществляется через ссылку «В главное меню».
Приложение извлекает все подпункты меню из БД по автогенерируемому слагу (slug) выбранного меню, которое берется из URL. Затем отображается это меню. При выборе пункта меню рекурсивно строится дерево подменю, содержащее все пункты меню текущего уровня вложенности и пункты следующего уровня. Этот список передается в шаблон для отображения, выполняя рекурсивные вызовы для отрисовки вложенных пунктов.
Таким образом, доступ к любому пункту меню возможен через указание слагов родительских пунктов и слагу искомого пункта в URL.

* <http://localhost/menu/3_menu/3_menu::level-1::item-3::sub_menu_name-oiun/3_menu::level-2::item-3::sub_menu_name-BTDl/>
