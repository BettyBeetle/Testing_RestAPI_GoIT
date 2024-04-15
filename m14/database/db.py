from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from m14.conf.config import settings



SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    '''
     Create a new database session.

    Yields:
        Session: The database session.
    '''
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()