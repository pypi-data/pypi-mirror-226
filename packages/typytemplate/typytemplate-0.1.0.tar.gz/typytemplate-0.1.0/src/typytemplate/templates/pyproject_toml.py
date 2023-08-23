from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the 'pyproject.toml' file with provided configuration"""
    return f"""
[tool.poetry]
name = "{kwargs["package_name"]}"
version = "{kwargs["version"]}"
description = "{kwargs["description"]}"
license = "{kwargs["license"]}"
authors = ["{kwargs["author"]}"]
readme = "README.md"
packages = [{{include = "{kwargs["package_name"]}", from = "src"}}]


[tool.poetry.dependencies]
python = "^{kwargs["python_version"]}"


[tool.black]
line-length = {kwargs["line_length"]}


[tool.ruff]
line-length = {kwargs["line_length"]}


[tool.pytest.ini_options]
pythonpath = ["."]


[tool.mypy]
strict = true
exclude = ["tests"]


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""".lstrip()
