_default:
    @just --list


VENV_CMD := if os() == "windows" {
    "venv\\Scripts\\activate"
} else {
    "source venv/bin/activate"
}

PYTEST_ARGS := "--asyncio-mode=auto"

# Run app. Use -d for dev mode
[group('run')]
[group('dev')]
[arg("dev", long, short='d', value="--dev", help="Run the app in dev mode")]
run dev='':
    @uv run textual run "{{dev}}" textual_system_monitor.app:Monitor


# Use Pytest to test the app, either wholly, or a subset of it
[group('testing')]
[arg("only", long, short='o', pattern='clicks|keys|buttons|color|bytes|misc|', help='Test the app')]
test only='':
    @echo ""
    uv run pytest {{PYTEST_ARGS}} {{ 
        if only == "color" { "tests/test_percent_color.py" }
        else if only != "" { "tests/test_" + only + ".py" }
        else { "tests" }
    }}


# Use Pytest to generate code coverage
[group('testing')]
cov:
    @echo ""
    @uv run pytest {{PYTEST_ARGS}} tests --cov=. --cov-branch


# Launch the Textual console. Used in debugging
[group('dev')]
console:
    @uv run textual console -x EVENT -x SYSTEM -x DEBUG


# If not using UV, install dependencies to a virtual env. Use -d to install dev dependencies, too
[group('util')]
[arg("dev", long, short='d', value="requirements_dev", help="Install dev dependencies, too")]
install dev='requirements':
    #!/usr/bin/env bash
    if command -v uv &> /dev/null; then
        echo "UV found. Install dependencies by running the app with 'just run'";
    else
        @echo "UV not found. Installing dependencies with pip..." &&
        @python3 -m venv venv && "{{VENV_CMD}}" &&
        @python3 -m pip3 install -r {{dev}}.txt;
    fi


# Show all files matching a type. Either src or tests
[group('util')]
[arg("kind", pattern='src|tests', help="Show all files matching a type")]
show kind:
    #!/usr/bin/env bash
    if [ {{kind}} == 'src' ]; then
        find src/textual_system_monitor -name "*.py" -not -name "__init__.py" -print
    else
        find tests -name "*.py" -not -name "__init__.py" -print
    fi


# Use Ruff to lint the whole project, given the rules in pyproject.toml
[group('util')]
lint:
    @uv run ruff check


# Use Ruff to format the whole project
[group('util')]
format:
    @uv run ruff format
