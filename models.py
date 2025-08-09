from sqlalchemy import Column , Integer , String, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime 

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key = True)
    user_id = Column(BigInteger, unique = True)
    username = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    responses = Column(Integer, default = 20)

class MessageHistr(Base):
    __tablename__ = 'MsgHistory'

    id = Column(Integer, primary_key = True)
    user_id = Column(BigInteger)
    message_text = Column(Text)
    date_of_message = Column(DateTime, default = datetime.utcnow)

