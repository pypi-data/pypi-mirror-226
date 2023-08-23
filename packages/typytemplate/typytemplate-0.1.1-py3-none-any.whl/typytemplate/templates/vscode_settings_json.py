from typing import Any


def format_file(**kwargs: dict[str, Any]) -> str:
    """Formats the VSCode 'settings.json' file with basic configuration"""
    return f"""
{{
    "editor.rulers": [
        {kwargs["line_length"]}
    ],
    "[python]": {{
        "editor.defaultFormatter": "ms-python.black-formatter",
    }},
    "mypy-type-checker.args": [
        "--config-file=${{workspaceFolder}}/pyproject.toml"
    ],
    "python.envFile": "${{workspaceFolder}}/.venv",
    "python.defaultInterpreterPath": "${{workspaceFolder}}/.venv/bin/python",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {{
        "source.organizeImports": true
    }},
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticSeverityOverrides": {{
        "reportPrivateUsage": "none",
        "reportMissingTypeStubs": "information",
        "reportUnknownVariableType": "none",
        "reportUntypedBaseClass": "none",
        "reportUnknownMemberType": "none",
        "reportUnknownArgumentType": "none",
        "reportGeneralTypeIssues": "none",
        "reportUntypedFunctionDecorator": "none"
    }},
}}
""".lstrip()
