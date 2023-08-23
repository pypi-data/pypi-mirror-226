from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the 'Makefile' file with basic commands"""
    return f"""
run:
\tpoetry run python -m {kwargs["package_name"]}.main

test:
\tpoetry run coverage run --source={kwargs["package_name"]} -m pytest -vv && \
poetry run coverage report --show-missing --skip-empty

lint:
\tpoetry run ruff ./ && poetry run pylint ./{kwargs["package_name"]} && poetry run mypy . --explicit-package-bases
""".lstrip()
