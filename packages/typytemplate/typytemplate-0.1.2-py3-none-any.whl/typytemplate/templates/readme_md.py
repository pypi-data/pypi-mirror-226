from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the 'README.md' file with basic project description"""
    return f"""
# {kwargs["package_name"]}

{kwargs["description"]}

🔨 **WIP**
""".lstrip()
