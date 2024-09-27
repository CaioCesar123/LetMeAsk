from pydantic import BaseModel
from typing import Optional

class NovoJogador(BaseModel):
    nome : str

class UpdateUsername(BaseModel):
    novoNome : str
    idJogador : int