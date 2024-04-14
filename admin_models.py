from typing import Optional
from sqlmodel import SQLModel, Field

# defining the Admin model using SQLModel
class Admin(SQLModel, table=True):
    # define fields with optional primary key
    admin_id: Optional[int] = Field(None, primary_key=True)
    admin_email: str  # admin's email address
    admin_name: str   # admin's name
    admin_password: str  # admin's password
