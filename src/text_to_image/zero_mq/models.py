import logging
from typing import Annotated, Literal, Optional

from PIL.Image import Image
from pydantic import BaseModel, Field, field_serializer, field_validator, ValidationInfo

from text_to_image.color import ColorPalette, Validation
from text_to_image.serialization.image import encode

logger = logging.getLogger(__name__)


class Request(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=250)]
    color: Optional[ColorPalette] = None

    @field_validator("color")
    @classmethod
    def ensure_color_format(cls, cp: Optional[ColorPalette], info: ValidationInfo):
        logger.debug("validating %s", cp)

        if cp is None:
            return None

        if not Validation.is_valid(cp["bg"]) or not Validation.is_valid(cp["text"]):
            raise ValueError(
                "Please use hex color formatting of either #xxx or #xxxyyy"
            )

        # add the octothorpe (#) if needed on fields
        for key in cp:
            value = cp[key]
            if not Validation.is_valid_with_hex_prefix(value):
                logger.debug("Adding octothorpe (#) prefix to %s color %s", key, value)
                cp[key] = f"#{value}"

        logger.debug("final color set: %s", cp)
        return cp


class SuccessReply(BaseModel):
    status: Literal["ok"] = "ok"
    image: Image

    @field_serializer("image")
    def image_serializer(self, image: Image) -> str:
        return encode(image)

    class Config:
        # so pydantic won't panic about Image
        arbitrary_types_allowed = True


class ErrorReply(BaseModel):
    status: Literal["error"] = "error"
    message: str
