import hmac
import os
from hashlib import sha256
from pathlib import Path

import git
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


BASE_DIR = Path(__file__).resolve().parent.parent


def _valid_github_signature(request):
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        return True

    signature = request.headers.get("X-Hub-Signature-256", "")
    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        request.body,
        sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


@csrf_exempt
def update(request):
    """Atualiza o código no PythonAnywhere quando o GitHub envia o webhook."""
    if request.method != "POST":
        return HttpResponse("Webhook ativo. Envie uma requisição POST para atualizar.")

    if not _valid_github_signature(request):
        return HttpResponseForbidden("Assinatura do webhook inválida.")

    repository_path = os.environ.get("BOOKSTORE_REPO_PATH", str(BASE_DIR))
    repo = git.Repo(repository_path)
    origin = repo.remotes.origin
    origin.pull("main")

    return HttpResponse("Updated code on PythonAnywhere")


def hello_world(request):
    template = loader.get_template("hello_world.html")
    return HttpResponse(template.render(request=request))
