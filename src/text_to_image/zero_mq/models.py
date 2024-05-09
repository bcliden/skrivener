from typing import Annotated, Literal

from PIL.Image import Image
from pydantic import (
    BaseModel,
    Field,
    field_serializer,
)

from text_to_image.serialization.image import encode


class Request(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=200)]


class SuccessReply(BaseModel):
    status: Literal["ok"] = "ok"
    image: Image

    @field_serializer("image")
    def image_serializer(self, image: Image) -> str:
        return encode(image)
    
    class Config:
        arbitrary_types_allowed = True


class ErrorReply(BaseModel):
    status: Literal["error"] = "error"
    message: str

