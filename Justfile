_default:
    @just --list


VENV_CMD := if os() == "windows" {
    "venv\\Scripts\\activate"
} else {
    "source venv/bin/activate"
}


# Run app. Use -d for dev mode
[group('run')]
[group('dev')]
[arg("dev", long, short='d', value="--dev", help="Run the app in dev mode")]
run dev='':
    @uv run textual run "{{dev}}" main.py


# Use Pytest to test the app, either wholly, or a subset of it
[group('testing')]
[arg("only", long, short='o', pattern='clicks|keys|buttons|color|bytes|misc|', help='Test the app')]
test only='':
    @echo ""
    uv run pytest --asyncio-mode=auto {{ 
        if only == "color" { "tests/test_percent_color.py" }
        else if only != "" { "tests/test_" + only + ".py" }
        else { "tests" }
    }}


# Use Pytest to generate code coverage
[group('testing')]
cov:
    @echo ""
    @uv run pytest --asyncio-mode=auto tests --cov=. --cov-branch


# Launch the Textual console. Used in debugging
[group('dev')]
console:
    @uv run textual console -x EVENT -x SYSTEM -x DEBUG


# Use Flake8 to lint the Python files
[group('dev')]
lint:
    @echo ""
    @uv run flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
    @uv run flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


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
        find . -path ./.venv -prune -o -path ./tests -prune -o -name "*.py" -not -name "__init__.py" -print
    else
        find tests -name "*.py" -not -name "__init__.py" -print
    fi


# Use Ruff to check the whole project, given the linter rules in pyproject.toml
[group('util')]
check:
    @uv run ruff check


# Use Ruff to format the whole project
[group('util')]
format:
    @uv run ruff format
