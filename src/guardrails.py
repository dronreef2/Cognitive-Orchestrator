"""Guardrails to enforce human-in-the-loop verification."""

from __future__ import annotations


def verify(message: str) -> bool:
    """Block execution until a human explicitly approves or rejects.

    Returns True when the user approves, False otherwise.
    """
    print("\n=== HUMAN VERIFICATION REQUIRED ===")
    print(message)
    while True:
        response = input("Proceed? [y/N]: ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no", ""}:
            return False
        print("Please answer with 'y' or 'n'.")
