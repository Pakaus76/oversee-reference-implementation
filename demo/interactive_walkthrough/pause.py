"""Pause helpers for the interactive walkthrough."""

from __future__ import annotations


def wait_for_user(message: str = "Press Enter to continue...") -> None:
    """Pause the walkthrough until the user presses Enter."""
    input(f"\n{message}")
