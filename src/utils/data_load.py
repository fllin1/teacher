"""
This module contains functions for loading and saving data.

Functions:
    save_progress(vocab: dict, path: Path) -> None
"""

import json


def save_progress(vocab, path):
    """
    Save progress to a JSON file.

    Args:
        vocab (dict): The vocabulary dictionary to save.
        path (Path): The path to the JSON file.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)
    print(f"Progress saved to {path}")
