SHELL := bash
.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: install
install:   ## Install dependencies
	@if command -v pipenv &> /dev/null; then \
	 echo "Pipenv found, installing dependencies with Pipenv..." && \
	 pipenv install; \
	else \
	 @echo "Pipenv not found, installing dependencies with pip..." && \
	 @pip install -r requirements.txt;
	fi


.PHONY: run
run:   ## Run app
	@pipenv run textual run main.py


.PHONY: run-dev
run-dev:   ## Run app in dev mode
	@pipenv run textual run --dev main.py


.PHONY: test
test:   ## Use Pytest to test the whole app
	@echo ""
	@pipenv run pytest tests


.PHONY: test-clicks
test-clicks:   ## Use Pytest to test the clicks only
	@echo ""
	@pipenv run pytest tests/test_clicks.py


.PHONY: test-keys
test-keys:   ## Use Pytest to test the key presses only
	@echo ""
	@pipenv run pytest tests/test_keys.py


.PHONY: test-buttons
test-buttons:   ## Use Pytest to test the buttons only
	@echo ""
	@pipenv run pytest tests/test_buttons.py


.PHONY: lint
lint:    ## Use Flake8 to lint the Python files
	@echo ""
	@pipenv run flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
	@pipenv run flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


.PHONY: console
console:  ## Show the Textual console. Used in debugging
	@pipenv run textual console -x EVENT -x SYSTEM -x DEBUG


.PHONY: show-tests
show-tests: $(test_files)   ## Show all test files
	@echo -e ""
	@find tests -name "*.py" -not -name "__init__.py" -print


.PHONY: show-src
show-src:  ## Show all source files
	@echo -e ""
	@find . -path ./.venv -prune -o -path ./tests -prune -o -name "*.py" -not -name "__init__.py" -print


.PHONY: hello
hello:  ## Show "Hello World"
	@echo -e "\nHello World"


.PHONY: help
help:   ## Show this help
	@echo -e "\nCommands:\n"
	@egrep '^[a-zA-Z_-]+:.*?## .*' Makefile | sort |
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
