from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DataBase = "sqlite:///database/LetMeAskDB.sqlite3"

engine = create_engine(DataBase)
Session = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base