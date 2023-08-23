from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the 'Makefile' file with basic commands"""
    return f"""
run:
\tpoetry run python -m src.{kwargs["package_name"]}.main

test:
\tpoetry run coverage run --source=src -m pytest -vv && poetry run coverage report --show-missing --skip-empty

lint:
\tpoetry run ruff ./ && poetry run pylint ./src && poetry run mypy . --explicit-package-bases
""".lstrip()
