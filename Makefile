SHELL := bash
.ONESHELL:
CWD = .
TEST_DIR := ./test
SRC_DIR := ./src


.PHONY: run
run:   ## Run app
	@textual run src/main.py


.PHONY: run-dev
run-dev:   ## Run app in dev mode
	@textual run --dev src/main.py


.PHONY: test
test:   ## Use Pytest to test the app
	@echo ""
	@pytest test


.PHONY: lint
lint:    ## Use Flake8 to lint the Python files
	@echo ""
	@flake8 src/*.py --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 src/*.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


.PHONY: console
console:  ## Show the Textual console. Used in debugging
	@textual console -x EVENT -x SYSTEM -x DEBUG


.PHONY: show-tests
test_files := $(TEST_DIR)/*.py
show-tests: $(test_files)   ## Show all tests
	@echo -e ""
	@echo $(subst test/, , $(filter-out test/__init__.py, $^))


.PHONY: show-src
source_files := $(SRC_DIR)/*.py
show-src: $(source_files)  ## Show all source files
	@echo -e ""
	@echo $(subst src/, , $(filter-out src/__init__.py, $^))


.PHONY: hello
hello:  ## Show "Hello World"
	@echo -e "\nHello World"


.PHONY: help
help:   ## Show this help
	@echo -e "\nCommands:\n"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
