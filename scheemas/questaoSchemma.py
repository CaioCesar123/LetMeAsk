from pydantic import BaseModel
from models.questoes import Questoes

class QuestionSchemma(BaseModel) :
    id : int

def make_quest(quest : Questoes):
    return{
        "pergunta": quest.questao,
        "alternativas": quest.alternativas,
        "tipo": quest.categoria
    }