import re

from typing_extensions import TypedDict


class ColorPalette(TypedDict):
    bg: str
    text: str


default_colors: list[ColorPalette] = [
    {"bg": "#2F3C7E", "text": "#FBEAEB"},  # pink on blue
    {"bg": "#F96167", "text": "#F9E795"},  # yellow on coral red
    # from dropbox.design:
    {"bg": "#0f503c", "text": "#cfafa2"},  # pink on green
    {"bg": "#0d2481", "text": "#e8e7aa"},  # pale lemon on blue
    {"bg": "#ceb4ff", "text": "#000000"},  # black on purple
    {"bg": "#9b0033", "text": "#FFFFFF"},  # white on maroon
    {"bg": "#f7f5f2", "text": "#1e1919"},  # brown on cream
    {"bg": "#b4c8e1", "text": "#1e1919"},  # brown on blue
]


class Validation:
    prefixed_color = re.compile(r"^#[\w\d]{3,6}$")
    non_prefixed_color = re.compile(r"^[\w\d]{3,6}$")

    @classmethod
    def is_valid_with_hex_prefix(cls, incoming: str) -> bool:
        return cls.prefixed_color.match(incoming)

    @classmethod
    def is_valid_no_hex_prefix(cls, incoming: str) -> bool:
        return cls.non_prefixed_color.match(incoming)

    @classmethod
    def is_valid(cls, incoming: str) -> bool:
        return cls.is_valid_with_hex_prefix(incoming) or cls.is_valid_no_hex_prefix(
            incoming
        )
