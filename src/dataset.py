"""
Module to build the vocabulary list from the docx files and scrape the
Chinese translation from the web.
"""

from pathlib import Path
import json
from tqdm import tqdm

from read_docx.data_processing import build_vocab_list
from scraping.chine_in import TraductionExtractor
from utils.data_load import save_progress


def main():
    """
    Main function
    """
    processed_path = Path("data/processed/chinese_vocab.json")

    if processed_path.exists():
        with open(processed_path, "r", encoding="utf-8") as f:
            existing_vocab = json.load(f)
    else:
        existing_vocab = {}

    all_vocab = build_vocab_list(vocab=existing_vocab, folder_path="data/raw")

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
        save_progress(all_vocab, processed_path)
        raise ConnectionError("Failed to fetch data. Progress has been saved.") from e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        save_progress(all_vocab, processed_path)
        raise RuntimeError("An error occurred. Progress has been saved.") from e

    save_progress(all_vocab, processed_path)


if __name__ == "__main__":
    main()
