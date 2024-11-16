"""
This module contains the functions to process the content of docx files and requests.

Functions:
    extract_vocab(text: str, vocab: dict) -> dict
    vocab_list(file_path: str, folder_path: str = "../data/raw") -> dict
    build_vocab_list(folder_path: str = "data/raw") -> dict
"""

import os

from read_docx.data_load import read_docx, get_files_name


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
    text = read_docx(os.path.join(folder_path, file_path))
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
    files_name = sorted(get_files_name(folder_path))

    for file_path in files_name:
        vocab = vocab_list(vocab=vocab, file_path=file_path, folder_path=folder_path)

    return vocab
