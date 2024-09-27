from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from typing import Union

class Jogadores(Base):
    __tablename__ = 'jogador'
    id = Column("jogador_pk", Integer, primary_key=True)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    nome = Column(String(200))

    sessoes = relationship('Sessoes', back_populates='jogador')

    def __init__(self, nome : str, inicio : Union[DateTime, None] = None, fim : Union[DateTime, None] = None):
        self.nome = nome
        if inicio :
            self.data_inicio = inicio
        if fim :
            self.data_fim = fim

