# =========================
# Imagem builder
# =========================
FROM python:3.13-slim AS builder

# Variáveis de ambiente do Python e Poetry
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Criar pasta do builder
WORKDIR $PYSETUP_PATH

# Instalar dependências do sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --upgrade pip && pip install poetry

# Copiar arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Instalar dependências do projeto (sem instalar o root)
RUN poetry install --no-root --without dev

# =========================
# Imagem final
# =========================
FROM python:3.13-slim AS runtime

# Variáveis de ambiente do Django e do venv
ENV VENV_PATH="/opt/pysetup/.venv" \
    PATH="/opt/pysetup/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=bookstore.settings

# Criar pasta da aplicação
WORKDIR /app

# Copiar venv do builder
COPY --from=builder /opt/pysetup/.venv /opt/pysetup/.venv

# Copiar o código do projeto
COPY . .

# Expor porta do Django
EXPOSE 8000

# Garantir que o Django encontre a aplicação
ENV PYTHONPATH=/app/bookstore

# Rodar servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
