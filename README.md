# Bookstore

Bookstore APP from Backend Python course from EBAC.

## Exercício - Django REST Framework

Este repositório contém a configuração solicitada na atividade da EBAC para adicionar o Django REST Framework (DRF) ao projeto `bookstore`.

A dependência `djangorestframework` está declarada no `pyproject.toml` e o app `rest_framework` está registrado em `INSTALLED_APPS` no arquivo `bookstore/settings.py`.

Comandos utilizados na atividade:

```shell
poetry add djangorestframework
poetry update
poetry run python manage.py check
poetry run python manage.py runserver
```

## Prerequisites

```text
Python 3.14+
Poetry
Docker && docker-compose
```

## Quickstart

1. Clone this project

   ```shell
   git clone https://github.com/julicorlando/bookstore.git
   ```

2. Install dependencies:

   ```shell
   cd bookstore
   poetry install
   ```

3. Run local dev server:

   ```shell
   poetry run python manage.py migrate
   poetry run python manage.py runserver
   ```

4. Run docker dev server environment:

   ```shell
   docker-compose up -d --build
   docker-compose exec web python manage.py migrate
   ```

5. Run tests inside of docker:

   ```shell
   docker-compose exec web python manage.py test
   ```
