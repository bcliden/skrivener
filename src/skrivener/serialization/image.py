import base64
import io

from PIL import Image as im
from PIL.Image import Image

"""
Image to b64
"""

png_options = {
    "optimize": True
}

def encode(image: Image) -> str:
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="png", **png_options)
    return base64_encode(img_bytes.getvalue())

def decode(encoded_image: str) -> Image:
    img_bytes = base64_decode(encoded_image)
    image = im.open(img_bytes)
    image.load()                # check to see if it's really usable I guess. maybe not needed
    return image

"""
slightly streamlined b64 en/decoding

credit to Pedro Lobito:
https://stackoverflow.com/a/60531872

after I had a little bit of trouble understanding the bytes args
"""

def base64_encode(s: bytes) -> str:
    return base64.b64encode(s).decode('utf-8')

def base64_decode(s: str) -> bytes:
    return base64.b64decode(s)