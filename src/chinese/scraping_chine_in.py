"""
This module contains the functions to scrape the Mandarin dictionary

Functions:
    generate_encoded_url(word: str) -> str
    search_mandarin_dictionary_requests(query: str) -> list

Classes:
    TraductionExtractor (object) -> Extract translations from search results
"""

import re

import requests
from bs4 import BeautifulSoup


def generate_encoded_url(word: str) -> str:
    """
    Generate the encoded URL for the word

    Args:
        word (str): The word to encode

    Returns:
        str: The encoded URL
    """
    base_url = "https://chine.in/mandarin/dictionnaire/index.php?mot="
    encoded_word = "".join([f"%26%23{ord(char)}%3B" for char in word])
    full_url = base_url + encoded_word
    return full_url


def search_mandarin_dictionary_requests(query: str) -> str:
    """
    Search the Mandarin dictionary using requests

    Args:
        query (str): The query to search

    Returns:
        str: The request response
    """
    url = generate_encoded_url(query)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
    }
    data = {"q": query, "Submit": "1"}

    response = requests.post(url, headers=headers, data=data, timeout=3)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all(class_="table invert_img", id="resultats_dico")
    return results[0]


class TraductionExtractor:
    """
    A class to extract translations from search results.

    Attributes:
        query (str): The query to search for translations.
    """

    def __init__(self, query: str):
        """
        Initializes the class with a query.

        Args:
            query (str): The query to search.
        """
        self.query = query
        self.results_raw = ""
        self.results_processed = ""

    # Treat HTML tags
    def fetch_results(self):
        """
        Fetches the search results for the query.
        """
        results_raw = search_mandarin_dictionary_requests(self.query)
        self.results_raw = str(results_raw)
        self.results_processed = results_raw.get_text()

    def remove_html_tags(self, text: list) -> list:
        """
        Removes the HTML tags from the text.

        Args:
            text (list): The text to remove the tags.

        Returns:
            list: The text without the tags.
        """
        return [re.sub(r"<.*?>", "", s) for s in text]

    # Process the results
    def extract_between_markers(
        self, result: str, start_marker: str, end_marker: str
    ) -> str:
        """
        Extracts the text between two markers.

        Args:
            start_marker (str): The starting marker.
            end_marker (str): The ending marker (optional).

        Returns:
            str: The extracted text, or None if not found.
        """
        start_index = result.find(start_marker)
        if start_index == -1:
            return None

        start_index += len(start_marker)
        if end_marker:
            end_index = result.find(end_marker, start_index)
            if end_index == -1:
                return None
            return result[start_index:end_index]
        else:
            return result[start_index:]

    # Get the translation
    def get_traduction(self) -> str:
        """
        Attempts to retrieve a translation from the results.

        Returns:
            str: The translation found, or None if no translation is available.
        """
        start_marker = f"Entrées pour {self.query}"
        end_marker = "Entrées commençant par"
        traduction = self.extract_between_markers(
            result=self.results_raw,
            start_marker=start_marker,
            end_marker=end_marker,
        )

        if not traduction:
            traduction = self.extract_between_markers(
                result=self.results_raw,
                start_marker="Traduction",
                end_marker="Editer (projet CFDICT)",
            )
        return traduction

    def return_traduction(self):
        """
        Returns the translation or indicates if no translation was found.
        """
        traduction = self.get_traduction()

        if traduction and "<li>" in traduction:
            traduction = traduction.split("</li>")[:-1]
        traduction = self.remove_html_tags(traduction)
        return traduction

    # Get the pinyin
    def get_pinyin(self) -> str:
        """
        Attempts to retrieve the pinyin from the results.

        Returns:
            str: The pinyin found, or None if no pinyin is available.
        """
        start_marker = "[ "
        end_marker = "]"
        pinyin = self.extract_between_markers(
            result=self.results_processed,
            start_marker=start_marker,
            end_marker=end_marker,
        )
        return pinyin


def main():
    """
    Test the TraductionExtractor class.
    """
    words = [
        {"chinese": "你好", "pinyin": "nǐ hǎo", "translation": "Bonjour"},
        {"chinese": "谢谢", "pinyin": "xièxie", "translation": "Merci"},
        {"chinese": "再见", "pinyin": "zàijiàn", "translation": "Au revoir"},
        {"chinese": "爱", "pinyin": "ài", "translation": "Amour"},
        {"chinese": "学习", "pinyin": "xuéxí", "translation": "Étudier"},
        {"chinese": "朋友", "pinyin": "péngyǒu", "translation": "Ami"},
        {"chinese": "快乐", "pinyin": "kuàilè", "translation": "Joie / Heureux"},
        {"chinese": "家", "pinyin": "jiā", "translation": "Maison / Famille"},
        {"chinese": "工作", "pinyin": "gōngzuò", "translation": "Travail"},
        {"chinese": "吃饭", "pinyin": "chīfàn", "translation": "Manger"},
    ]
    for word in words:
        query = word["chinese"]
        extractor = TraductionExtractor(query)
        extractor.fetch_results()
        traduction = extractor.return_traduction()
        pinyin = extractor.get_pinyin()
        print(
            "\n Query:",
            query,
            "\n Translation GPT4:",
            word["translation"],
            "; Translation found:",
            traduction,
            "\n Pinyin GPT4:",
            word["pinyin"],
            "; Pinyin found:",
            pinyin,
        )


if __name__ == "__main__":
    main()
