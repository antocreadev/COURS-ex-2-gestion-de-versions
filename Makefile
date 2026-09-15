# Raccourcis du projet. `make aide` liste les cibles.
# La cible clé est `make check` : elle joue EXACTEMENT ce que joue la CI.

PYTHON  ?= python3
VENV    := .venv
BIN     := $(VENV)/bin

.DEFAULT_GOAL := aide
.PHONY: aide install hooks format lint types test check clean

aide: ## Affiche cette aide
	@echo "Cibles disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Crée l'environnement virtuel et installe le projet + les outils
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e ".[dev]"
	@echo "\nEnvironnement prêt. Pensez à : make hooks"

hooks: ## Installe les hooks Git (pre-commit, commit-msg, pre-push)
	$(BIN)/pre-commit install --install-hooks
	@echo "\nHooks installés. Test à blanc : $(BIN)/pre-commit run --all-files"

format: ## Reformate le code
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

lint: ## Vérifie le style sans modifier les fichiers
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

types: ## Vérifie les types (mypy strict)
	$(BIN)/mypy

test: ## Lance les tests avec la couverture
	$(BIN)/pytest

check: lint types test ## Tout ce que fait la CI, en local
	@echo "\n\033[32mTout est vert — vous pouvez ouvrir votre Pull Request.\033[0m"

clean: ## Supprime les fichiers générés
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
