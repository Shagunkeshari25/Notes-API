from typing import List, Optional, ForwardRef
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Note Schemas
class NoteBase(BaseModel):
    title: str
    body: str

class NoteCreate(NoteBase):
    pass

class ShowNote(NoteBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2 replacement for orm_mode

# Forward reference for nested creator
ShowUser = ForwardRef("ShowUser")

class ShowNoteWithCreator(ShowNote):
    creator: ShowUser


# User Schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    email: EmailStr

class ShowUser(UserBase):
    id: int
    notes: List[ShowNote] = []

    model_config = {"from_attributes": True}

# Fix forward references
ShowNoteWithCreator.update_forward_refs()

# Auth Schemas
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None