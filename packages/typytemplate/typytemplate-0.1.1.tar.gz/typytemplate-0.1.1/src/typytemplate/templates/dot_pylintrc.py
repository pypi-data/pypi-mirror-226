from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the '.pylintrc' file with basic Pylint configuration"""
    return f"""
[MASTER]
max-line-length={kwargs["line_length"]}
disable=
    C0114, # missing-module-docstring
    C0115, # missing-class-docstring
    C0116, # missing-function-docstring

good-names=1
ignored-modules=
""".lstrip()
