from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from typing import Union

class Sessoes(Base):
    __tablename__ = 'sessao'
    id = Column("sessao_pk", Integer, primary_key=True)
    pontuacao_sessao = Column(Integer)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    tema_id = Column(Integer)
    tema_name = Column(String(200))

    resposta_jogador = relationship('Resposta_Jogador', back_populates='sessao') 

    jogador_id = Column(Integer, ForeignKey('jogador.jogador_pk'))
    jogador = relationship('Jogadores', back_populates='sessoes')

    def __init__(self, pontuacao_jogador : int, id_tema = int, nome_tema = str, inicio : Union[DateTime, None] = None, fim : Union[DateTime, None] = None):
        self.pontuacao_sessao = pontuacao_jogador
        self.tema_id = id_tema
        self.tema_name = nome_tema
        if inicio :
            self.data_inicio = inicio
        if fim :
            self.data_fim = fim
            