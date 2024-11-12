import os

from utils.data_load import get_files_name
from utils.data_processing import vocab_list


def build_vocab_list(folder_path: str = "data/raw") -> dict:
    """
    Get the vocabulary list from the docx file

    Args:
        file_path (str): The file path of the docx file
        folder_path (str, optional): The folder path. Defaults to "../data/raw".

    Returns:
        dict: The vocabulary dictionary
    """
    files_name = sorted(get_files_name(folder_path))
    vocab = {}

    for file_path in files_name:
        vocab = vocab_list(vocab=vocab, file_path=file_path, folder_path=folder_path)

    return vocab


def main():
    vocab = build_vocab_list()
    print(vocab)


if __name__ == "__main__":
    main()
