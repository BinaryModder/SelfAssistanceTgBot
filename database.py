
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 
 

def InitDatabase(database_url) :
    
    engine = create_engine(database_url, pool_size = 10, max_overflow = 5, pool_pre_ping = True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)

    return Session()

