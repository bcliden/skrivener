from typing import Optional
from PIL import Image as im
from PIL import ImageFont
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from importlib.resources import files

Coords = tuple[int, int, int, int]

default_size = (512, 512)
bg = "FFF"
text = "000"
padding = 10
font = files('text_to_image.font').joinpath('Super Creamy Personal Use.ttf').read_bytes()

"""
need a font...
also let's consider using imagemagick if it's rly bad
"""


def set_text(text: str) -> Image:
    i = im.new("RGB", default_size)
    draw = ImageDraw(i)

    # draw bg
    coords: Coords = (
        0 + padding,
        0 + padding,
        default_size[0] - padding,
        default_size[1] - padding,
    )
    height = coords[2] - coords[0]
    width = coords[3] - coords[1]

    draw.rectangle(coords, fill=bg)

    font_size = 100  # or some other max
    size: Optional[Coords] = None

    font = ImageFont.truetype("font/Super Creamy Personal Use.ttf")

    while (
        size is None or size[0] > height or size[1] > width
    ) or font_size > 0:
        # reduce font
        font = font.font_variant(size=font_size)

        # check if it fits
        size = draw.multiline_textbbox((coords[0], coords[1]), text, font=font)

        # subtract one?
        font_size -= 1

    draw.multiline_text((coords[0], coords[1]), text, font)

    return i
