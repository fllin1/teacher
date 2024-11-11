"""
This module contains the functions to scrape the Mandarin dictionary

Functions:
    generate_encoded_url(word: str) -> str
    search_mandarin_dictionary_requests(query: str) -> list
"""

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


def search_mandarin_dictionary_requests(query: str) -> list:
    """
    Search the Mandarin dictionary using requests

    Args:
        query (str): The query to search

    Returns:
        list: The list of results
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

    return results
