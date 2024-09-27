from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from .base import Base
from .jogador import Jogadores
from .questoes import Questoes
from .resposta_jogador import Resposta_Jogador
from .sessoes import Sessoes

project = "database/"

if not os.path.exists(project):
    os.mkdir(project)

db_path = os.path.join(project, 'LetMeAskDB.sqlite3')

db_url = f'sqlite:///{db_path}'

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url) :
    create_database(engine.url)

Base.metadata.create_all(bind=engine)