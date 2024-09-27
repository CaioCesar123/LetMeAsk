from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Resposta_Jogador(Base):
    __tablename__ = "respostas"
    id = Column("respostas_pk", Integer, primary_key=True)
    resposta_jogador = Column(String(200))
    resposta_correta = Column(Boolean)

    sessao_id = Column(Integer, ForeignKey('sessao.sessao_pk'))
    sessao = relationship('Sessoes', back_populates='resposta_jogador')

    questao_id = Column(Integer, ForeignKey('questao.questao_pk'))
    questao = relationship('Questoes', back_populates='resposta_jogador')

    def __init__(self, resposta: str, resposta_certa: bool, sessao_id: int, questao_id: int):
        self.resposta_jogador = resposta
        self.resposta_correta = resposta_certa
        self.sessao_id = sessao_id
        self.questao_id = questao_id