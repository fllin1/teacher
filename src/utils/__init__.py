"""
This module initializes the utils package.

Modules:
    data_load
    data_processing
    data_save
    dict_scraping

Functions:
    read_docx
    get_files_name
    extract_vocab
    vocab_list
    save_data
    generate_encoded_url
    search_mandarin_dictionary_requests
"""

from .data_load import read_docx, get_files_name
from .data_processing import extract_vocab, vocab_list
from .data_save import save_data
from .dict_scraping import generate_encoded_url, search_mandarin_dictionary_requests

__all__ = [
    "read_docx",
    "get_files_name",
    "extract_vocab",
    "vocab_list",
    "save_data",
    "generate_encoded_url",
    "search_mandarin_dictionary_requests",
]
