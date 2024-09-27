from pydantic import BaseModel

class RespostaSchemma(BaseModel):
    id_questao : int
    id_sessao : int
    resposta : str

class AnswerInput(BaseModel):
    resposta: str
    questao_id: int
    sessao_id: int