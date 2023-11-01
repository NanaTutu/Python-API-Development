from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' - format for connecting to pg db via url
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #Responsible for establishing database connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Responsible for creating sessions and committing

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()