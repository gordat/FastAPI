from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from modules.database import Base

class App(Base):
    __tablename__ = 'myAPI'
    
    ID = Column(Integer, primary_key=True, index=True)
    Server = Column(String)
    Name = Column(String)
    Pos = Column(String)
    Path = Column(String)
    Port = Column(Integer)
    Enabled = Column(Boolean)
    Required = Column(Boolean)
    LastCommands = Column(String)
    Running = Column(Boolean)
    Pid = Column(Integer)
    Material = Column(String)
    Order = Column(String)
    Message = Column(String)


class User(Base):
    __tablename__ = 'users'    
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
