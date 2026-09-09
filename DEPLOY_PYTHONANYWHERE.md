# Deploy do Bookstore no PythonAnywhere

Este guia acompanha o projeto final de Continuous Delivery da EBAC.

## 1. Criar a aplicação no PythonAnywhere

1. Crie uma conta no PythonAnywhere.
2. Abra um console Bash.
3. Clone o repositório:

```bash
git clone https://github.com/julicorlando/bookstore.git
cd bookstore
git checkout main
```

4. Crie e ative um ambiente virtual compatível com a versão Python disponível na conta:

```bash
python3 -m venv ~/env
source ~/env/bin/activate
python -m pip install --upgrade pip
pip install poetry
poetry install
```

## 2. Configurar o Web App

No painel `Web` do PythonAnywhere:

- escolha `Manual configuration`;
- configure `Source code` para a pasta do repositório;
- configure `Working directory` para a mesma pasta;
- informe o caminho do virtualenv, por exemplo `/home/SEU_USUARIO/env`;
- edite o arquivo WSGI para carregar `bookstore.wsgi.application`.

O `settings.py` aceita o host via variável de ambiente e também permite subdomínios `pythonanywhere.com` por padrão.

## 3. Variáveis de ambiente

Configure no ambiente do PythonAnywhere os valores adequados ao seu projeto:

```text
SECRET_KEY=<uma-chave-segura>
DEBUG=0
DJANGO_ALLOWED_HOSTS=SEU_USUARIO.pythonanywhere.com
BOOKSTORE_REPO_PATH=/home/SEU_USUARIO/bookstore
GITHUB_WEBHOOK_SECRET=<segredo-opcional-do-webhook>
```

Caso use PostgreSQL, configure também:

```text
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<database>
SQL_USER=<usuario>
SQL_PASSWORD=<senha>
SQL_HOST=<host>
SQL_PORT=5432
```

Sem `SQL_ENGINE`, o projeto usa SQLite como fallback.

## 4. Rotas usadas no exercício

Após o deploy:

```text
https://SEU_USUARIO.pythonanywhere.com/hello/
https://SEU_USUARIO.pythonanywhere.com/update_server/
```

A rota `/update_server/` recebe o webhook do GitHub e executa `git pull main` no repositório configurado por `BOOKSTORE_REPO_PATH`.

## 5. Configurar o webhook no GitHub

No repositório, acesse:

`Settings -> Webhooks -> Add webhook`

Use:

```text
Payload URL: https://SEU_USUARIO.pythonanywhere.com/update_server/
Content type: application/json
Secret: o mesmo valor de GITHUB_WEBHOOK_SECRET, se configurado
Evento: Just the push event
Active: marcado
```

Depois do merge na `main`, o webhook notificará a aplicação no PythonAnywhere para atualizar o código.

## 6. GitHub Actions

O workflow de CI executa em Pull Requests para `main` e também em commits enviados à `main`, validando a configuração do Django e executando os testes antes da entrega.
