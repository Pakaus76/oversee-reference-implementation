"""Console display helpers for the interactive walkthrough."""

from __future__ import annotations


def print_title(title: str) -> None:
    """Print a main title for the walkthrough."""
    line = "=" * len(title)
    print(f"\n{line}")
    print(title)
    print(line)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n--- {title} ---")


def print_bullets(items: list[str]) -> None:
    """Print a simple bullet list."""
    for item in items:
        print(f"- {item}")


def print_key_values(values: dict[str, object]) -> None:
    """Print key-value pairs in a readable way."""
    for key, value in values.items():
        print(f"{key}: {value}")


def print_source_inputs(inputs: list[dict[str, str]]) -> None:
    """Print enterprise source inputs for one layer."""
    for index, item in enumerate(inputs, start=1):
        source = item.get("source", "unknown source")
        information = item.get("information", "no information")
        print(f"{index}. {source}")
        print(f"   -> {information}")
