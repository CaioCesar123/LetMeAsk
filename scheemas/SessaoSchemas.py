from pydantic import BaseModel
from typing import Optional

class SessaoInput(BaseModel):
    jogador_id: int
    tema: str
    id_tema : int

class SessaoOutput(BaseModel):
    message: str
    id_sessao: int

class SessaoDelet(BaseModel):
    idSessao : int
