def format_file() -> str:
    """Formats the '.gitignore' file with usual ignore patterns"""
    return """
.venv/

__pycache__
dist

.mypy_cache/
.ruff_cache/

/.coverage
/.pytest_cache
/htmlcov
""".lstrip()
