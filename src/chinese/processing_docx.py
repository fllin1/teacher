"""
This module contains the functions to process the content of docx files and requests.

Functions:
    extract_vocab(text: str, vocab: dict) -> dict
    vocab_list(file_path: str, folder_path: str = "../data/raw") -> dict
    build_vocab_list(folder_path: str = "data/raw") -> dict

Main function:
    main()

Usage:
    To process the docx files and request the translations:
    $ python -m src.chinese.processing_docx
"""

import json
import os
from pathlib import Path

from tqdm import tqdm

from src.chinese.scraping_chine_in import TraductionExtractor
from src.utils.data import File, Read, Save


def extract_vocab(text: str, vocab: dict) -> dict:
    """
    Extract the vocabulary from the text

    Args:
        text (str): The text to extract the vocabulary
        vocab (dict): The vocabulary dictionary

    Returns:
        dict: The vocabulary dictionary
    """

    for word in text:
        word = "".join(e for e in word if e.isalnum())
        word.replace(" ", "")
        if word not in vocab and 0 < len(word) < 12 and "2024" not in word:
            vocab[word] = {}
    return vocab


def vocab_list(vocab: str, file_path: str, folder_path: str = "../data/raw") -> dict:
    """
    Get the vocabulary list from the docx file

    Args:
        file_path (str): The file path of the docx file
        folder_path (str, optional): The folder path. Defaults to "../data/raw".

    Returns:
        dict: The vocabulary dictionary
    """
    text = Read.read_docx(os.path.join(folder_path, file_path))
    extracted_vocab = extract_vocab(text.split(" "), vocab)
    return extracted_vocab


def build_vocab_list(vocab: dict = None, folder_path: str = "data/raw") -> dict:
    """
    Get the vocabulary list from the docx file

    Args:
        vocab (dict, optional): The vocabulary dictionary. Defaults to {}.
        folder_path (str, optional): The folder path. Defaults to "../data/raw".

    Returns:
        dict: The vocabulary dictionary
    """
    files_name = sorted(File.file_name("docx", folder_path))

    for file_path in files_name:
        vocab = vocab_list(vocab=vocab, file_path=file_path, folder_path=folder_path)

    return vocab


def main():
    """
    Main function
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    processed_path = os.path.join(base_dir, "data", "raw", "chinese_vocab.json")

    if processed_path.exists():
        with open(processed_path, "r", encoding="utf-8") as f:
            existing_vocab = json.load(f)
    else:
        existing_vocab = {}

    all_vocab = build_vocab_list(
        vocab=existing_vocab, folder_path=os.path.join(base_dir, "data/raw")
    )

    try:
        for word in tqdm(all_vocab.keys(), desc="Processing vocabulary", unit="word"):
            if all_vocab[word] == {}:
                extractor = TraductionExtractor(word)
                extractor.fetch_results()
                traduction = extractor.return_traduction()
                pinyin = extractor.get_pinyin()
                all_vocab[word]["traduction"] = traduction
                all_vocab[word]["pinyin"] = pinyin
    except ConnectionError as e:
        print(f"Connection error occurred: {e}")
        Save.save_json(all_vocab, processed_path)
        raise ConnectionError("Failed to fetch data. Progress has been saved.") from e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        Save.save_json(all_vocab, processed_path)
        raise RuntimeError("An error occurred. Progress has been saved.") from e

    Save.save_json(all_vocab, processed_path)


if __name__ == "__main__":
    main()
