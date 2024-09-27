from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Questoes(Base):
    __tablename__ = 'questao'
    id = Column("questao_pk",Integer, primary_key=True)
    questao = Column(String(700))
    resposta_correta = Column(String(300))
    alternativas = Column(JSON)
    dificuldade = Column(String(100))
    categoria = Column(String(200))

    resposta_jogador = relationship('Resposta_Jogador', back_populates='questao')

    def __init__(self, quest : str,quest_resposta : str, quest_alternativas : list, dificuldade : str, categoria:str ):
        self.questao = quest
        self.resposta_correta = quest_resposta
        self.alternativas = quest_alternativas
        self.dificuldade = dificuldade
        self.categoria = categoria
