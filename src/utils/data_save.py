"""
This module contains the functions to save the data.

Functions:
    save_data(data: dict, path: str) -> None
"""

import pandas as pd


def save_data(data: dict, path: str) -> None:
    """
    Save the data to a csv file

    Args:
        data (dict): The data to save
        path (str): The path to save the data
    """
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
