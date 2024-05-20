import logging
import random
from typing import Optional
from importlib.resources import as_file

from PIL import Image as im
from PIL import ImageFont
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageColor import getrgb

from skrivener.color import ColorPalette, default_colors
from skrivener.font import default_font

# types
Coords = tuple[int, int, int, int]

# globals
logger = logging.getLogger(__name__)

# defaults
default_size = (512, 512)
padding = 50


def height(c: Coords) -> int:
    x0, _, x1, _ = c
    return x1 - x0


def width(c: Coords) -> int:
    _, y0, _, y1 = c
    return y1 - y0


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int) -> str:
    """
    I was going to use python's textwrap, but ttf fonts are not monospace.

    I used this lovely algorithm instead:
    https://stackoverflow.com/a/67203353
    """
    lines = [""]
    for word in text.split():
        line = f"{lines[-1]} {word}".strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return "\n".join(lines)


def set_text(text: str, color: Optional[ColorPalette] = None) -> Image:
    i = im.new("RGB", default_size)
    draw = ImageDraw(i)

    if color is None:
        color = random.choice(default_colors)
    logger.debug("using colors bg=%s txt=%s", color["bg"], color["text"])

    # Draw the full width background color
    canvas: Coords = (
        0,
        0,
        default_size[0],
        default_size[1],
    )
    draw.rectangle(canvas, fill=getrgb(color["bg"]))

    # get the interior (padded) dimensions
    interior_canvas: Coords = (
        canvas[0] + padding,
        canvas[1] + padding,
        canvas[2] - padding,
        canvas[3] - padding,
    )
    x0, y0, *_ = interior_canvas
    logger.debug("interior canvas size: %s", interior_canvas)

    with as_file(default_font) as font_file:
        logger.debug("loading font: %s", font_file)
        font = ImageFont.truetype(font_file)

    # begin looking for ideal font size
    font_size = 50
    wrapped_text_size: Optional[Coords] = None

    while (
        wrapped_text_size is None
        # the wrapped text doesn't fit in the canvas
        or width(wrapped_text_size) > width(interior_canvas)
        or height(wrapped_text_size) > height(interior_canvas)
    ) and font_size > 0:
        font = font.font_variant(size=font_size)
        wrapped = get_wrapped_text(text, font, width(interior_canvas))
        wrapped_text_size = draw.multiline_textbbox(
            xy=(x0, y0), text=wrapped, font=font
        )
        font_size -= 2

    if font_size <= 0:
        raise ValueError(f"Could not fit text in {default_size} image at any size.")

    if wrapped_text_size is None:
        raise ValueError("Dunno, just felt like it (wrapped text is still none)")

    logger.debug("drawing text with font size=%s", font_size)

    draw.multiline_text(
        xy=(x0, y0),
        text=wrapped,
        fill=getrgb(color["text"]),
        font=font,
    )

    return i
