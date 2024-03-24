SHELL := bash
.ONESHELL:

.PHONY: run
run:   ## Run app
	@textual run main.py


.PHONY: run-dev
run-dev:   ## Run app in dev mode
	@textual run --dev main.py


.PHONY: test
test:   ## Use Pytest to test the app
	@echo ""
	@pytest tests


.PHONY: lint
lint:    ## Use Flake8 to lint the Python files
	@echo ""
	@flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


.PHONY: console
console:  ## Show the Textual console. Used in debugging
	@textual console -x EVENT -x SYSTEM -x DEBUG


.PHONY: show-tests
show-tests: $(test_files)   ## Show all tests
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
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort |
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
