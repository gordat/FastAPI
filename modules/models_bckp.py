from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class App(Base):
    __tablename__ = 'myAPI'
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Pos = Column(String)
    Path = Column(String)
    Port = Column(Integer)
    Enabled = Column(Boolean)
    Required = Column(Boolean)    
    LastCommands = relationship("Commands", back_populates="LastCommands")
    Running = Column(Boolean)
    Pid = Column(Integer)
    Material = Column(String)
    Order = Column(String)
    Message = Column(String)
    cmd_id = Column(Integer, ForeignKey("commands.id"))

class Commands(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    cmd1 = Column(String)
    cmd2 = Column(String)
    cmd3 = Column(String)
    cmd4 = Column(String)
    cmd5 = Column(String)
    cmd6 = Column(String)
    cmd7 = Column(String)
    cmd8 = Column(String)
    cmd9 = Column(String)
    cmd10 = Column(String)
    LastCommands = relationship("App", back_populates="LastCommands")

class User(Base):
    __tablename__ = 'users'    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
