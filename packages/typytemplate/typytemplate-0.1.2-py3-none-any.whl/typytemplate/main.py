import argparse
import os
import subprocess
import sys
from os.path import join as path_join
from subprocess import Popen
from typing import Any

from typytemplate.templates import (
    dot_gitignore,
    dot_pylintrc,
    main_py,
    makefile,
    pyproject_toml,
    readme_md,
    test_main_py,
    vscode_settings_json,
)

TERM_COL_CYAN = "\033[36m"
TERM_COL_LIGHT_GREEN = "\033[92m"
TERM_COL_RESET = "\033[0m"


def create_init_file(directory: str) -> None:
    create_file(directory, "__init__.py", "")


def create_file(directory: str, path: str, content: str) -> None:
    os.makedirs(directory, exist_ok=True)
    with open(path_join(directory, path), "xt", encoding="utf-8") as file:
        file.write(content)


def run_command(directory: str, command: tuple[str, ...]) -> tuple[int, str, str]:
    with Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory) as process:
        stdout, stderr = process.communicate()
        return (process.returncode, stdout.decode(), stderr.decode())


def install_poetry_deps(directory: str) -> None:
    run_command(directory, ("poetry", "add", "black", "ruff", "mypy", "pylint", "--group", "dev"))
    run_command(directory, ("poetry", "add", "pytest", "coverage", "--group", "test"))


def get_git_username() -> str:
    author = ""
    ret, stdout, _ = run_command(os.getcwd(), ("git", "config", "--get", "user.name"))
    if ret == 0:
        author = stdout.strip()
        ret, stdout, _ = run_command(os.getcwd(), ("git", "config", "--get", "user.email"))
        if ret == 0:
            author += f" <{stdout.strip()}>"
    return author


def get_user_prompts(project_dir: str) -> dict[str, Any]:
    config = {}
    prompts = [
        ("Package Name", str, project_dir),
        ("Version", str, "0.0.1"),
        ("Description", str, ""),
        ("license", str, ""),
        ("Author", str, get_git_username()),
        ("Line Length", int, 120),
    ]
    for desc, data_type, default in prompts:
        key = desc.lower().replace(" ", "_")
        while True:
            try:
                user_value = input(
                    f"{TERM_COL_CYAN}{desc} [{TERM_COL_LIGHT_GREEN}{default}{TERM_COL_CYAN}]: {TERM_COL_RESET}"
                )
                config[key] = data_type(user_value) if user_value else default
                break
            except ValueError:
                ...
    return config


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="Typy: Python project templating",
        description="Automatically create templated Python program using command-line wizzard.",
    )
    parser.add_argument("project_dir")
    cmd_args = vars(parser.parse_args())
    base_dir = path_join(os.getcwd(), cmd_args["project_dir"])

    config = get_user_prompts(cmd_args["project_dir"])
    config["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}"

    create_file(base_dir, "pyproject.toml", pyproject_toml.format_file(**config))
    create_file(base_dir, ".pylintrc", dot_pylintrc.format_file(**config))
    create_file(base_dir, "Makefile", makefile.format_file(**config))
    create_file(base_dir, "README.md", readme_md.format_file(**config))
    create_file(base_dir, ".gitignore", dot_gitignore.format_file())

    vscode_dir = path_join(base_dir, ".vscode")
    create_file(vscode_dir, "settings.json", vscode_settings_json.format_file(**config))

    project_dir = path_join(base_dir, config["package_name"])
    create_init_file(project_dir)
    create_file(project_dir, "main.py", main_py.format_file())

    tests_dir = path_join(base_dir, "tests")
    init_py_content = 'import pytest\n\npytest.register_assert_rewrite("conftest")\n'
    create_file(tests_dir, "__init__.py", init_py_content)
    create_file(tests_dir, "conftest.py", "")
    create_file(tests_dir, "test_main.py", test_main_py.format_file(**config))

    install_poetry_deps(base_dir)

    print(f"\n{TERM_COL_LIGHT_GREEN}✓ All done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
