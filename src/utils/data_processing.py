"""
This module contains the functions to process the docx files

Functions:
    extract_vocab(text: str, vocab: dict) -> dict
    vocab_list(file_path: str, folder_path: str = "../data/raw") -> dict
"""

import os

from src.utils.data_load import read_docx


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
        if word.startswith(" "):
            word = word[1:]
        if word not in vocab and 0 < len(word) < 12:
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
    text = read_docx(os.path.join(folder_path, file_path))
    extracted_vocab = extract_vocab(text.split(" "), vocab)
    return extracted_vocab
