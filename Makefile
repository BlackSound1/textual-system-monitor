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
install:  ## Install dependencies to a virtual env, if not using UV
	@if command -v uv &> /dev/null; then \
	 echo "UV found. Install dependencies by running the app with 'make run'"; \
	else \
	 @echo "UV not found. Installing dependencies with pip..." && \
	 @python3 -m venv venv && "$(VENV_CMD)" && \
	 @python3 -m pip3 install -r requirements.txt;
	fi


.PHONY: install-dev
install-dev:  ## Install ALL dependencies to a virtual env, if not using UV
	@if command -v uv &> /dev/null; then \
	 echo "UV found. Install dependencies by running the app with 'make run'"; \
	else \
	 @echo "UV not found. Installing dependencies with pip..." && \
	 @python3 -m venv venv && "$(VENV_CMD)" && \
	 @python3 -m pip3 install -r requirements.txt && python3 -m pip3 install -r requirements_dev.txt;
	fi


.PHONY: run
run:  ## Run app
	@uv run textual run textual_system_monitor.app:Monitor


.PHONY: run-dev
run-dev:  ## Run app in dev mode
	@uv run textual run --dev textual_system_monitor.app:Monitor


.PHONY: test
test:  ## Use Pytest to test the whole app
	@echo ""
	@uv run pytest $(PYTEST_ARGS) tests


.PHONY: test-%
test-%:  ## Use Pytest to test parts of the app (clicks, keys, buttons, color, bytes, misc)
	@valid_targets="clicks keys buttons color bytes misc"; \
	target=$(subst test-,,$@); \
	if ! echo "$$valid_targets" | grep -q "$$target"; then \
		echo "Error: Invalid test target '$$target'. Valid options: $$valid_targets"; \
		exit 1; \
	fi; \
	echo ""; \
	uv run pytest $(PYTEST_ARGS) $(if $(filter test-color, $@), tests/test_percent_color.py, tests/test_$(subst test-,,$@).py)


.PHONY: cov
cov:  ## Use Pytest to generate code coverage
	@echo ""
	@uv run pytest --asyncio-mode=auto tests --cov=. --cov-branch


.PHONY: lint
lint:  ## Use Ruff to lint the whole project, given the rules in pyproject.toml
	@uv run ruff check


.PHONY: lint-fix
lint-fix:  ## Use Ruff to lint the whole project, given the rules in pyproject.toml. Then fix errors
	@uv run ruff check --fix


.PHONY: format
format:  ## Use Ruff to format the whole project
	@uv run ruff format


.PHONY: console
console:  ## Show the Textual console. Used in debugging
	@uv run textual console -x EVENT -x SYSTEM -x DEBUG


.PHONY: show-tests
show-tests: $(test_files)  ## Show all test files
	@echo -e ""
	@find tests -name "*.py" -not -name "__init__.py" -print


.PHONY: show-src
show-src:  ## Show all source files
	@echo -e ""
	@find src/textual_system_monitor -name "*.py" -not -name "__init__.py" -print


.PHONY: help
help:  ## Show this help
	@echo -e "\nCommands:\n"
	@egrep '^[%a-zA-Z_-]+:.*?## .*' Makefile | sort |
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
