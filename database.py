from sqlalchemy import create_engine, Column , Integer , String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime 




Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key = True)
    telegram_id = Column(Integer, unique = True)
    username = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))

class MessageHistr(Base):
    __tablename__ = 'MsgHistory'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    message_text = Column(Text)
    message_by_bot = Column(Text)
    date_of_message = Column(DateTime, default = datetime.utcnow)
    

def InitDatabase(database_url):
    
    engine = create_engine(database_url, pool_size = 10, max_overflow = 5, pool_pre_ping = True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)

    return Session()

