#from quiz_backend.utils.imports import TypedDict, timedelta
from datetime import timedelta
from typing import TypedDict

# define type for access and refresh token
TokenType = TypedDict(
    "TokenType",
    {
        "user_name": str,
        "user_email": str,
        "access_expiry_time": timedelta,
        "refresh_expiry_time": timedelta

    }
)