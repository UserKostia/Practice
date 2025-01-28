from pydantic import BaseModel, Field
from typing import Optional, Any


class SuccessResponse(BaseModel):
    """
    Shema for successful responses.

    :param
    message: Message about the success.
    data: Additional data (optional).
    """
    message: str = Field(...)
    data: Optional[Any] = Field(None)


class ErrorResponse(BaseModel):
    """
    Schema for error responses.

    :param
    error: Short error description.
    details: Additional error details (optional).
    """
    error: str = Field(...)
    details: Optional[Any] = Field(None)
