default:
    @just --list


VENV_CMD := if os() == "windows" {
    "venv\\Scripts\\activate"
} else {
    "source venv/bin/activate"
}

# Install dependencies to a virtual env, if not using UV
[group('installing')]
install:
    @if command -v uv &> /dev/null; then \
        echo "UV found. Install dependencies by running the app with 'just run'"; \
    else \
        @echo "UV not found. Installing dependencies with pip..." && \
        @python3 -m venv venv && "{{VENV_CMD}}" && \
        @python3 -m pip3 install -r requirements.txt;
    fi

# Install ALL dependencies to a virtual env, if not using UV
[group('installing')]
[group('dev')]
install-dev:
    @if command -v uv &> /dev/null; then \
        echo "UV found. Install dependencies by running the app with 'make run'"; \
    else \
        @echo "UV not found. Installing dependencies with pip..." && \
        @python3 -m venv venv && "{{VENV_CMD}}" && \
        @python3 -m pip3 install -r requirements.txt && python3 -m pip3 install -r requirements_dev.txt;
    fi


# Run app normally or in dev mode
[group('run')]
[group('dev')]
[arg("dev", long, short='d', value="--dev", help="Run the app in dev mode")]
run dev='':
    @uv run textual run "{{dev}}" main.py

# Use Pytest to test the whole app
[group('testing')]
test:
	@echo ""
	@uv run pytest tests


# Use Pytest to test the clicks only
[group('testing')]
test-clicks:
	@echo ""
	@uv run pytest tests/test_clicks.py


# Use Pytest to test the key presses only
[group('testing')]
test-keys:
	@echo ""
	@uv run pytest tests/test_keys.py


# Use Pytest to test the buttons only
[group('testing')]
test-buttons:
	@echo ""
	@uv run pytest tests/test_buttons.py


# Use Pytest to generate code coverage
[group('testing')]
cov:
	@echo ""
	@uv run pytest tests --cov=. --cov-branch


# Show the Textual console. Used in debugging
[group('dev')]
console:
	@uv run textual console -x EVENT -x SYSTEM -x DEBUG


# Use Flake8 to lint the Python files
[group('dev')]
lint:
	@echo ""
	@uv run flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
	@uv run flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

