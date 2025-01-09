from typing import Literal

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Token schema.

    :param
    access_token: The access token.
    token_type: The type of token.
    """
    access_token: str = Field(...)
    token_type: Literal["bearer"] = Field(default="bearer")
