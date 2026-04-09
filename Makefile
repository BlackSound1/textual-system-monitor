SHELL := bash
.ONESHELL:
.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	VENV_CMD := "venv\Scripts\activate"
else
	VENV_CMD := "source venv/bin/activate"
endif

PYTEST_ARGS := "--asyncio-mode=auto"


.PHONY: install
install:   ## Install dependencies to a virtual env, if not using UV
	@if command -v uv &> /dev/null; then \
	 echo "UV found. Install dependencies by running the app with 'make run'"; \
	else \
	 @echo "UV not found. Installing dependencies with pip..." && \
	 @python3 -m venv venv && "$(VENV_CMD)" && \
	 @python3 -m pip3 install -r requirements.txt;
	fi


.PHONY: install-dev
install-dev:   ## Install ALL dependencies to a virtual env, if not using UV
	@if command -v uv &> /dev/null; then \
	 echo "UV found. Install dependencies by running the app with 'make run'"; \
	else \
	 @echo "UV not found. Installing dependencies with pip..." && \
	 @python3 -m venv venv && "$(VENV_CMD)" && \
	 @python3 -m pip3 install -r requirements.txt && python3 -m pip3 install -r requirements_dev.txt;
	fi


.PHONY: run
run:   ## Run app
	@uv run textual run main.py


.PHONY: run-dev
run-dev:   ## Run app in dev mode
	@uv run textual run --dev main.py


.PHONY: test
test:   ## Use Pytest to test the whole app
	@echo ""
	@uv run pytest $(PYTEST_ARGS) tests


.PHONY: test-%
test-%:   ## Use Pytest to test parts of the app
	@echo ""
	@uv run pytest $(PYTEST_ARGS) $(if $(filter test-%, $@), \
		$(if $(filter test-color, $@), tests/test_percent_color.py, \
		tests/test_$(subst test-,,$@).py), \
		tests)


.PHONY: cov
cov:   ## Use Pytest to generate code coverage
	@echo ""
	@uv run pytest --asyncio-mode=auto tests --cov=. --cov-branch


.PHONY: lint
lint:    ## Use Flake8 to lint the Python files
	@echo ""
	@uv run flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
	@uv run flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


.PHONY: check
check:    ## Use Ruff to check the whole project, given the linter rules in pyproject.toml
	@uv run ruff check


.PHONY: format
format:    ## Use Ruff to format the whole project
	@uv run ruff format


.PHONY: console
console:  ## Show the Textual console. Used in debugging
	@uv run textual console -x EVENT -x SYSTEM -x DEBUG


.PHONY: show-tests
show-tests: $(test_files)   ## Show all test files
	@echo -e ""
	@find tests -name "*.py" -not -name "__init__.py" -print


.PHONY: show-src
show-src:  ## Show all source files
	@echo -e ""
	@find . -path ./.venv -prune -o -path ./tests -prune -o -name "*.py" -not -name "__init__.py" -print


.PHONY: help
help:   ## Show this help
	@echo -e "\nCommands:\n"
	@egrep '^[%a-zA-Z_-]+:.*?## .*' Makefile | sort |
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
