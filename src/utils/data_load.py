import os

from docx import Document


def get_files_name(folder_path: str = "../data/raw"):
    """
    Get all the files in the folder_path

    Args:
        folder_path (str, optional): The folder path. Defaults to "../data/raw".

    Returns:
        list: List of files in the folder_path
    """
    return [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".docx")
    ]


def read_docx(file_path: str):
    """
    Read the docx file and return the full text

    Args:
        file_path (str): The file path of the docx file

    Returns:
        str: The full text of the docx file
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return " ".join(full_text)
