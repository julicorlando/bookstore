# Pulse — Clone funcional de microblog

Projeto final de rede social inspirado em plataformas de microblog, desenvolvido com **Python, Django e Django REST Framework**.

## Requisitos atendidos

- cadastro e login seguros usando autenticação nativa do Django;
- edição opcional de nome, usuário, e-mail, foto, bio e senha;
- seguir/deixar de seguir usuários;
- páginas de seguidores e seguindo;
- feed com publicações apenas das pessoas seguidas;
- criação e exclusão das próprias publicações;
- curtidas e comentários;
- interface responsiva com Django Templates + CSS;
- API REST com cadastro, token, perfil, feed, posts, comentários, follow e like;
- suporte a SQLite local e PostgreSQL em produção;
- testes automatizados e workflow de CI.

## Executar localmente

```bash
cd twitter_clone
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
# source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`.

## API REST

- `POST /api/register/` — criar conta
- `POST /api/login/` — obter token
- `GET/PATCH /api/me/` — perfil autenticado
- `GET /api/feed/` — feed dos usuários seguidos
- `GET/POST /api/posts/` — listar/criar posts
- `GET/PUT/PATCH/DELETE /api/posts/{id}/`
- `GET/POST /api/comments/`
- `POST /api/users/{username}/follow/` — seguir/deixar de seguir
- `POST /api/posts/{id}/like/` — curtir/descurtir

Para endpoints protegidos use:

```text
Authorization: Token SEU_TOKEN
```

## PostgreSQL

Defina as variáveis `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` e `POSTGRES_PORT`. Sem elas, o projeto utiliza SQLite.

## Deploy

O projeto está pronto para hospedagem em um serviço Python com WSGI (PythonAnywhere, Render, Railway, VPS etc.). Configure:

```text
SECRET_KEY=uma-chave-forte
DEBUG=0
ALLOWED_HOSTS=seu-dominio.com
```

Depois execute `python manage.py migrate` e `python manage.py collectstatic --noinput` e inicie com `gunicorn socialnet.wsgi:application` a partir da pasta `twitter_clone`.

> O link público do deploy deve ser adicionado aqui após a criação do serviço de hospedagem.
