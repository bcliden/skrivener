import logging
from typing import Optional
from time import sleep
from PIL import Image as im
from PIL import ImageFont
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageColor import getrgb
from importlib.resources import as_file, files

Coords = tuple[int, int, int, int]

logger = logging.getLogger(__name__)


default_size = (800, 600)
color = {"bg": "#a37a74", "text": "#e49273"}
padding = 50

default_font = files("text_to_image.font").joinpath("Super Creamy Personal Use.ttf")


"""
need a font...
also let's consider using imagemagick if it's rly bad
"""


def height(c: Coords) -> int:
    offset_y, offset_x, len_y, len_x = c
    return len_y - offset_y


def width(c: Coords) -> int:
    offset_y, offset_x, len_y, len_x = c
    return len_x - offset_x


def set_text(text: str) -> Image:
    i = im.new("RGB", default_size)
    draw = ImageDraw(i)

    # draw bg
    canvas: Coords = (
        0 + padding,
        0 + padding,
        default_size[0] - padding,
        default_size[1] - padding,
    )

    draw.rectangle(canvas, fill=getrgb(color["bg"]))

    font_size = 50  # or some other max
    size: Optional[Coords] = None

    with as_file(default_font) as font_file:
        logger.info("loading font: %s", font_file)
        font = ImageFont.truetype(font_file)
    # font = ImageFont.truetype('arial.ttf')

    while (
        size is None or height(size) > height(canvas) or width(size) > width(canvas)
    ) and font_size > 0:
        font = font.font_variant(size=font_size)
        size = draw.multiline_textbbox((canvas[0], canvas[1]), text, font=font)
        logger.info("size is: %s", size)
        font_size -= 1

        if font_size == 0:
            raise ValueError("too much text for the screen I guess")

    if size is None:
        # just to satisfy mypy really
        raise ValueError("dunno, size was still None")
    
    logger.info("fit text size: %s", size)
    logger.info("canvas size: %s", canvas)
    logger.info("drawing text with font size=%s", font_size)
    draw.multiline_text(
        xy=(size[0], size[1]),
        text=text,
        fill=getrgb(color["text"]),
        font=font,
    )

    return i
