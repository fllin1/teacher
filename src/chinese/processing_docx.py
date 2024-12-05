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

from tqdm import tqdm

from src.chinese.scraping import (
    get_pinyin,
    google_traduction_extractor,
    ChineInTranslator,
)
from src.utils.data import File, Read, Save


class ProcessDocx:
    """
    A class to process the content of docx files and requests.

    Functions:
        extract_vocab(text: str, vocab: dict) -> dict
        vocab_list(file_path: str, folder_path: str = "../data/raw") -> dict
        build_vocab_list(folder_path: str = "data/raw") -> dict
    """

    def __init__(self, list_characters: set, vocab: list):
        """
        Initialize the object with the list of characters and the vocabulary.

        Args:
            list_characters (set): The set of characters to exclude.
            vocab (list): The list of vocabulary words.
        """
        self.list_characters = list_characters
        self.vocab = vocab
        self.folder_path = "data/raw"
        self.files_name = sorted(File.file_name("docx", self.folder_path))

    def extract_vocab(self, text: str) -> dict:
        """
        Extract the vocabulary from the text

        Args:
            self (object): The object
            text (str): The text to extract the vocabulary

        Returns:
            dict: The vocabulary dictionary
        """

        for word in text:
            word = "".join(e for e in word if e.isalnum())
            word.replace(" ", "")
            if (
                word not in self.list_characters
                and 0 < len(word) < 12
                and "2024" not in word
            ):
                self.vocab.append(
                    {"character": word, "traduction": [""], "pronunciation": ""}
                )
        return self.vocab

    def vocab_list(
        self,
        file_path: str,
    ) -> dict:
        """
        Get the vocabulary list from the docx file

        Args:
            self (object): The object
            file_path (str): The file path of the docx file

        Returns:
            dict: The vocabulary dictionary
        """
        text = Read.read_docx(os.path.join(self.folder_path, file_path))
        extracted_vocab = self.extract_vocab(text.split(" "))
        return extracted_vocab

    def build_vocab_list(self) -> dict:
        """
        Get the vocabulary list from the docx file

        Args:
            self (object): The object

        Returns:
            dict: The vocabulary dictionary
        """
        for file_path in self.files_name:
            vocab = self.vocab_list(
                file_path=file_path,
            )

        return vocab


def main():
    """
    Main function
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    processed_path = os.path.join(base_dir, "data", "processed", "chinese_vocab.json")
    checkpoint_path = os.path.join(
        base_dir, "data", "interim", "chinese_vocab_checkpoint.json"
    )

    if os.path.exists(processed_path):
        with open(processed_path, "r", encoding="utf-8") as f:
            existing_vocab = json.load(f)
    else:
        existing_vocab = []

    list_characters = set()
    for vocab in existing_vocab:
        list_characters.add(vocab["character"])

    processor = ProcessDocx(list_characters=list_characters, vocab=existing_vocab)
    all_vocab = processor.build_vocab_list()

    try:
        for index in tqdm(
            range(len(all_vocab)), desc="Processing vocabulary", unit="word"
        ):
            vocab = all_vocab[index]
            word = vocab["character"]
            if vocab["traduction"] == [""]:
                extractor = ChineInTranslator(word)
                traduction = extractor.return_traduction()
                if traduction == [""]:
                    traduction = google_traduction_extractor(word)
                all_vocab[index]["traduction"] = traduction
            if not vocab["pronunciation"]:
                all_vocab[index]["pronunciation"] = get_pinyin(word)
    except ConnectionError as e:
        print(f"Connection error occurred: {e}")
        Save.save_json(all_vocab, checkpoint_path)
        raise ConnectionError("Failed to fetch data. Progress has been saved.") from e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        Save.save_json(all_vocab, checkpoint_path)
        raise RuntimeError("An error occurred. Progress has been saved.") from e

    Save.save_json(all_vocab, processed_path)


if __name__ == "__main__":
    main()
