from typing import NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    """https://hakibenita.com/python-mypy-exhaustive-checking"""
    assert False, f"Unhandled value: {value} ({type(value).__name__})"
