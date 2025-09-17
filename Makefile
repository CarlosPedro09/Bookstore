# ==========================
# Makefile atualizado - Projeto Bookstore
# ==========================

# Versão do Python
PYTHON_VERSION ?= 3.13

# Diretórios contendo módulos do projeto
LIBRARY_DIRS = bookstore order product

# Build artifacts
BUILD_DIR ?= build

# PyTest opções
PYTEST_HTML_OPTIONS = --html=$(BUILD_DIR)/report.html --self-contained-html
PYTEST_COVERAGE_OPTIONS = --cov=$(LIBRARY_DIRS)
PYTEST_OPTIONS ?= $(PYTEST_HTML_OPTIONS) $(PYTEST_COVERAGE_OPTIONS)

# Poetry
POETRY ?= poetry
RUN_PYPKG_BIN = $(POETRY) run

# Cores para saída no terminal
COLOR_ORANGE = \033[33m
COLOR_RESET = \033[0m

# ==========================
# Utilitários
# ==========================

.PHONY: help
help:  ## Mostra esse help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: version-python
version-python:  ## Mostra a versão do Python
	@echo $(PYTHON_VERSION)

# ==========================
# Testes
# ==========================

.PHONY: test
test:  ## Roda os testes do projeto
	$(RUN_PYPKG_BIN) pytest $(PYTEST_OPTIONS) order/tests product/tests

# ==========================
# Build e publicações
# ==========================

.PHONY: build
build:  ## Build do pacote via Poetry
	$(POETRY) build

.PHONY: publish
publish:  ## Publica pacote no repositório configurado
	$(POETRY) publish

.PHONY: deps
deps:  ## Instala todas as dependências do projeto via Poetry
	$(POETRY) install

# ==========================
# Qualidade de código
# ==========================

.PHONY: check
check: check-py  ## Checa linting e type hints

.PHONY: check-py
check-py: check-flake8 check-black check-mypy

.PHONY: check-flake8
check-flake8:  ## Roda flake8
	$(RUN_PYPKG_BIN) flake8 .

.PHONY: check-black
check-black:  ## Roda black (modo check)
	$(RUN_PYPKG_BIN) black --check --line-length 118 .

.PHONY: check-mypy
check-mypy:  ## Roda mypy
	$(RUN_PYPKG_BIN) mypy $(LIBRARY_DIRS)

.PHONY: format
format: format-black format-isort  ## Formata código

.PHONY: format-black
format-black:
	$(RUN_PYPKG_BIN) black .

.PHONY: format-isort
format-isort:
	$(RUN_PYPKG_BIN) isort $(LIBRARY_DIRS)

# ==========================
# Docker / Django
# ==========================

.PHONY: migrate
migrate:  ## Roda migrações no container web
	docker-compose exec web python manage.py migrate --noinput

.PHONY: seed
seed:  ## Roda seed (popula DB)
	docker-compose exec web python manage.py seed
