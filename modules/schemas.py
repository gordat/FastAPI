from pydantic import BaseModel
from typing import Optional, List

class AppItem(BaseModel):   
    ID: int
    Server: str
    Name: str
    Pos: str
    Path: str
    Port: int
    Enabled: bool
    Required: bool
    LastCommands: List[str] = []
    Running: bool
    Pid: int
    Material: str
    Order: str
    Message: str

class UpdateAppItem(BaseModel):   
    # ID: Optional[int] = None
    Server: Optional[str] = None
    Name: Optional[str] = None
    Pos: Optional[str] = None
    Path: Optional[str] = None
    Port: Optional[int] = None
    Enabled: Optional[bool] = None
    Required: Optional[bool] = None
    LastCommands: Optional[List[str]] = None
    Running: Optional[bool] = None
    Pid: Optional[int] = None
    Material: Optional[str] = None
    Order: Optional[str] = None
    Message: Optional[str] = None

class ShowCommands(BaseModel):
    commands: List[str]
    class Config():
        orm_mode = True

class ShowItem(AppItem):    
    class Config():
        orm_mode = True

class ShowUpdatedItem(UpdateAppItem):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None