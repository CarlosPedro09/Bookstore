from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git
import os


@csrf_exempt
def update(request):
    """Webhook do GitHub para atualizar o código no servidor (git pull)."""
    if request.method == "POST":
        try:
            # Ajuste o caminho para o diretório correto do seu projeto
            repo_dir = "/home/Carlos09/Bookstore"
            if os.path.exists(repo_dir):
                repo = git.Repo(repo_dir)
                origin = repo.remotes.origin
                origin.pull()
                return HttpResponse("✅ Código atualizado com sucesso no PythonAnywhere.")
            else:
                return HttpResponse("❌ Diretório do repositório não encontrado.", status=500)
        except Exception as e:
            return HttpResponse(f"⚠️ Erro ao atualizar: {str(e)}", status=500)

    return HttpResponse("Método não permitido. Use POST.", status=405)


def hello_world(request):
    """Página de teste simples."""
    template = loader.get_template("hello_world.html")
    return HttpResponse(template.render({}, request))
