from typing import Optional
from sqlmodel import SQLModel, Field

# create login model
class LoginModel(SQLModel):
    user_email: str
    user_password: str

# create pydantic model for user
class UserModel(LoginModel):
    user_name: str
    # user_email: str
    # user_password: str

# Define User model
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(None, primary_key=True)
    
# Define Token model
class Token(SQLModel, table=True):
    token_id: Optional[int] = Field(None, primary_key=True)
    user_id : int = Field(int, foreign_key="user.user_id")  # add fk :- save refresh token with user-id
    refresh_token: str  # refresh token for authentication



