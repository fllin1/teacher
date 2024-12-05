"""
This module provides classes to manage Chinese vocabulary cards, parse definitions, and filter
cards by category.

Classes:
    Card (object) -> Represents a single vocabulary card with Chinese characters and related
    information
    CardManager (object) -> Manages a collection of Card objects and provides methods to load,
    filter, and save them
    DefinitionParser (object) -> Parses Chinese word definitions into structured categories,
    definitions, and examples

Functions:
    Card:
        __init__(
            self,
            character: str,
            pronunciation: str,
            traduction: str = None,
            category: str = None,
            score: str = None,
            difficulty: str = None,
            correct: str = None,
            incorrect: str = None,
            reviewed: str = None,
        )
        to_dict(self) -> Dict[str, Any]

    CardManager:
        __init__(self)
        load_cards_from_xml(self, xml_path: str)
        remove_cards_by_categories(self, keywords: Union[List[str], str])
        get_cards_data(self) -> List[Dict[str, Any]]
        _convert_to_list(value: Any) -> List[Any]

    DefinitionParser:
        parse_definition(definition: str) -> Union[Dict[str, List[Dict[str, List[str]]]], str]
        _split_definitions(text: str) -> List[Dict[str, List[str]]]

Main function:
    main()

Usage:
    python -m src.chinese.processing_xml
"""

import os
import re
from typing import Any, Dict, List, Union
from xml.etree import ElementTree as ET

from src.utils.data import Save, File


class Card:
    """
    Represents a single vocabulary card with Chinese characters and related information.
    """

    def __init__(
        self,
        character: str,
        pronunciation: str,
        traduction: str = None,
        category: str = None,
        score: str = None,
        difficulty: str = None,
        correct: str = None,
        incorrect: str = None,
        reviewed: str = None,
    ):
        self.character = character
        self.pronunciation = pronunciation
        self.traduction = traduction
        self.category = category
        self.score = score
        self.difficulty = difficulty
        self.correct = correct
        self.incorrect = incorrect
        self.reviewed = reviewed

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the card's data to a dictionary.

        Returns:
            Dict[str, Any]: The card's data as a dictionary.
        """
        return {
            "character": self.character,
            "pronunciation": self.pronunciation,
            "traduction": self.traduction,
            "category": self.category,
            "score": self.score,
            "difficulty": self.difficulty,
            "correct": self.correct,
            "incorrect": self.incorrect,
            "reviewed": self.reviewed,
        }


class CardManager:
    """
    Manages a collection of Card objects and provides methods to load, filter, and save them.
    """

    def __init__(self):
        self.cards: List[Card] = []

    def load_cards_from_xml(self, xml_path: str):
        """
        Loads cards from an XML file.

        Args:
            xml_path (str): Path to the XML file containing the cards.
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for card_elem in root.find("cards").findall("card"):
            entry = card_elem.find("entry")

            catassign = card_elem.find("catassign")
            category = catassign.attrib["category"] if catassign is not None else None
            score_info = card_elem.find("scoreinfo")
            traduction = entry.find("defn")

            card = Card(
                character=entry.find("headword").text,
                pronunciation=entry.find("pron").text,
                traduction=traduction.text if traduction is not None else None,
                category=category,
                score=score_info.attrib.get("score")
                if score_info is not None
                else None,
                difficulty=score_info.attrib.get("difficulty")
                if score_info is not None
                else None,
                correct=score_info.attrib.get("correct")
                if score_info is not None
                else None,
                incorrect=score_info.attrib.get("incorrect")
                if score_info is not None
                else None,
                reviewed=score_info.attrib.get("reviewed")
                if score_info is not None
                else None,
            )

            self.cards.append(card)

    def remove_cards_by_categories(self, keywords: Union[List[str], str]):
        """
        Removes cards where the category contains any of the specified keywords.

        Args:
            keywords (Union[List[str], str]): A keyword or list of keywords to match against the category.
        """
        keywords = self._convert_to_list(keywords)
        keywords = [k.lower() for k in keywords]

        filtered_cards = []
        for card in self.cards:
            if card.category:
                category_lower = card.category.lower()
                if any(keyword in category_lower for keyword in keywords):
                    continue  # Skip cards matching the keywords
            filtered_cards.append(card)

        self.cards = filtered_cards

    def get_cards_data(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of cards as dictionaries.

        Returns:
            List[Dict[str, Any]]: The list of card data.
        """
        return [card.to_dict() for card in self.cards]

    @staticmethod
    def _convert_to_list(value: Any) -> List[Any]:
        """
        Converts the input value to a list if it is not already a list.

        Args:
            value (Any): The input value, which can be of any type.

        Returns:
            List[Any]: The value converted to a list.
        """
        if not isinstance(value, list):
            value = [value]
        return value


class DefinitionParser:
    """
    Parses Chinese word definitions into structured categories, definitions, and examples.
    """

    @staticmethod
    def parse_definition(
        definition: str,
    ) -> Union[Dict[str, List[Dict[str, List[str]]]], str]:
        """
        Parses a Chinese word definition into structured categories, definitions, and examples.

        Args:
            definition (str): The raw definition text.

        Returns:
            Union[Dict[str, List[Dict[str, List[str]]]], str]: A dictionary where each key is a part of speech,
            and each value is a list of definitions with their examples, or the original definition if parsing fails.
        """
        parts_of_speech = [
            "adjective",
            "adverb",
            "affix",
            "auxiliary",
            "idiom",
            "noun",
            "preposition",
            "pronoun",
            "surname",
            "verb",
        ]

        pos_pattern = r"\b(" + "|".join(parts_of_speech) + r")\b"
        matches = list(re.finditer(pos_pattern, definition, re.IGNORECASE))

        if not matches:
            return definition

        parsed_data = {}

        positions = [match.start() for match in matches] + [len(definition)]
        parts = [match.group(1).lower() for match in matches]

        for idx, pos in enumerate(positions[:-1]):
            current_pos = parts[idx]
            start_idx = pos
            end_idx = positions[idx + 1]
            text = definition[start_idx:end_idx].strip()
            # Remove the part of speech from the beginning
            text = re.sub(
                r"^\b" + re.escape(current_pos) + r"\b", "", text, flags=re.IGNORECASE
            ).strip()
            definitions = DefinitionParser._split_definitions(text)
            parsed_data[current_pos] = definitions

        return parsed_data

    @staticmethod
    def _split_definitions(text: str) -> List[Dict[str, List[str]]]:
        """
        Splits the text into individual definitions and their examples.

        Args:
            text (str): The text containing definitions and examples.

        Returns:
            List[Dict[str, List[str]]]: A list of dictionaries with 'definition' and 'examples'.
        """
        definitions = []
        # Split numbered definitions or different entries
        def_splits = re.split(r"(?=\d+\s)", text)
        for def_text in def_splits:
            def_text = def_text.strip()
            if not def_text:
                continue
            # Extract the definition number if it exists
            match = re.match(r"^(\d+)\s", def_text)
            if match:
                def_number = match.group(1)
                def_text = def_text[len(def_number) :].strip()
            else:
                def_number = None
            # Split the definition and examples
            example_splits = re.split(r"(?<=\.)\s+", def_text)
            definition = example_splits[0]
            examples = example_splits[1:] if len(example_splits) > 1 else []
            # Clean up the examples
            examples = [ex.strip() for ex in examples if ex.strip()]
            definitions.append(
                {
                    "definition": definition,
                    "examples": examples,
                }
            )
        return definitions


def main():
    """
    Main function
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(
        base_dir,
        "data/raw/",
        File.file_name("xml", "data/raw")[-1],
    )

    card_manager = CardManager()
    card_manager.load_cards_from_xml(file_path)

    categories_to_remove = ["Cours1 ", "Cours2 ", "Cours3 ", "Question Answer Voca"]
    card_manager.remove_cards_by_categories(categories_to_remove)

    cards_data = [card.to_dict() for card in card_manager.cards]
    Save.save_json(
        file=cards_data,
        path=os.path.join(base_dir, "data/processed/chinese_pleco.json"),
    )


if __name__ == "__main__":
    main()
