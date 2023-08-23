def format_file() -> str:
    """Formats the 'main.py' file with basic 'Hello World' structure"""
    return """
import sys


def main() -> int:
    print("Hello World!")
    return 0


if __name__ == "__main__": # pragma: no cover
    sys.exit(main())
""".lstrip()
