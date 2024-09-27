from flask import Flask, redirect,jsonify
from flask_openapi3 import Info, OpenAPI, Tag
from flask_cors import CORS
from models import Session,Jogadores, Sessoes, Questoes,Resposta_Jogador
from datetime import datetime
import config
from scheemas.jogadorSchema import NovoJogador,UpdateUsername
from scheemas.SessaoSchemas import SessaoInput,SessaoDelet
from scheemas.questaoSchemma import QuestionSchemma, make_quest
from scheemas.RespostaSchema import RespostaSchemma,AnswerInput
import requests

import html
from googletrans import Translator

info = Info(title="Let me Ask", version="1.0")
app = OpenAPI(__name__, info=info)
app.config.from_object(config)
CORS(app)

home = Tag(name="Jogadores", description="Manipulação de Jogadores")
sessao = Tag(name="Sessão", description="Manipulação de Sessão")
perguntas = Tag(name="Perguntas", description="Buscar as categorias e as perguntas")
respostas = Tag(name="Resposta", description="Salvar Resposta dos jogadores")


@app.post('/criar_jogador', tags=[home])
def criar_jogador(form  : NovoJogador):
    session = Session()
    try:
        # Criação do jogador
        novo_jogador = Jogadores(
            nome=form.nome,
            inicio=datetime.now(), 
            fim=datetime.now() 
        )
        session.add(novo_jogador)
        session.commit()
        return {"message": "Jogador criado com sucesso", "jogador_id": novo_jogador.id}, 200
    except Exception as e:
        session.rollback()
        return {"error": str(e)}, 400
    
@app.get('/categorias', tags=[perguntas])
def get_categories():
    url = "https://opentdb.com/api_category.php"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            categories = data['trivia_categories']
            # Retorna apenas os nomes das categorias e seus ids
            return jsonify(categories), 200
        else:
            return {"error": "Não foi possível obter as categorias"}, 400
    except Exception as e:
        return {"error": f"Ocorreu um erro: {str(e)}"}, 500
    
@app.post('/start_session', tags=[sessao])
def start_session(form: SessaoInput):
    session = Session()

    jogador = session.query(Jogadores).filter(Jogadores.id == form.jogador_id).first()

    if not jogador:
        error_msg = "Usuario não encontrado."
        return {"message": error_msg}, 400
    
    sessao = Sessoes(
        pontuacao_jogador= 0,
        id_tema= form.id_tema,
        nome_tema= form.tema,
        fim=datetime.now(),
        inicio=datetime.now()
    )

    sessao.jogador = jogador

    try:
        session.add(sessao)
        session.commit()
        return {"message": "Sessão Iniciada"}, 200
    except Exception as e:
        session.rollback()
        error_msg = "Algo deu errado"
        return {"message": error_msg}, 400
    
@app.post('/buscar_pergunta', tags=[perguntas])
def fetch_question(form: QuestionSchemma):
    session = Session()
    translator = Translator()

    # Buscar a sessão ativa
    sessao = session.query(Sessoes).filter(Sessoes.id == form.id).first()
    
    if not sessao:
        return {"message": "Sessão não encontrada"}, 400
    
    # # Configurar a URL para a requisição da pergunta
    url = f"https://opentdb.com/api.php?amount=1&category={sessao.tema_id}&difficulty=easy&type=multiple"

    try:
        # Fazer a requisição à API
        response = requests.get(url)
        print(response)
        
        if response.status_code == 200:
            data = response.json()
            question = data['results'][0]

            questao_texto = html.unescape(question['question'])
            resposta_correta = html.unescape(question['correct_answer'])
            alternativas = [html.unescape(alt) for alt in question['incorrect_answers']] + [resposta_correta]
            categoria = html.unescape(question['category'])

            questao_texto_traduzido = translator.translate(questao_texto, src='en', dest='pt').text
            resposta_correta_traduzida = translator.translate(resposta_correta, src='en', dest='pt').text
            alternativas_traduzidas = [translator.translate(alt, src='en', dest='pt').text for alt in alternativas]
            categoria_traduzido = translator.translate(categoria, src='en', dest='pt').text
            
            # Montar os dados da pergunta
            questao = Questoes(
                quest=questao_texto_traduzido,
                quest_resposta=resposta_correta_traduzida,
                quest_alternativas=alternativas_traduzidas,
                dificuldade="easy",
                categoria=categoria_traduzido
            )
            
            # Salvar a pergunta no banco
            session.add(questao)
            session.commit()

            # Retornar a pergunta para o usuário
            return make_quest(questao), 200

        else:
            return {"message": "Erro ao buscar pergunta da API"}, 400

    except Exception as e:
        session.rollback()
        return {"message": "Erro interno ao buscar a pergunta"}, 500
    
@app.post('/answer_question', tags=[respostas])
def answer_question(form: AnswerInput):
    session = Session()

    # Buscar a questão correspondente
    questao = session.query(Questoes).filter(Questoes.id == form.questao_id).first()
    if not questao:
        return {"message": "Questão não encontrada"}, 404
    
    sessao = session.query(Sessoes).filter(Sessoes.id == form.sessao_id).first()
    if not sessao:
        return {"message": "Sessão não encontrada"}, 404

    if (questao.resposta_correta == form.resposta):
        sessao.pontuacao_sessao += 1 

    sessao.data_fim = datetime.now() 

    resposta_jogador = Resposta_Jogador(
        resposta=form.resposta,
        resposta_certa= (form.resposta == questao.resposta_correta),
        sessao_id=sessao.id,
        questao_id=questao.id 
    )

    try:
        session.add(resposta_jogador)
        session.commit()

        if (form.resposta == questao.resposta_correta):
            return jsonify({"resultado": "correto"}), 200
        else: 
            return jsonify({"resultado": "errado"}), 200

    except Exception as e:
        session.rollback()
        return {"message": "Erro ao processar a resposta"}, 400

from flask import jsonify

@app.put('/update_username', tags=[home])
def update_username(form: UpdateUsername):
    session = Session()

    # Buscar o jogador pelo ID
    jogador = session.query(Jogadores).filter(Jogadores.id == form.idJogador).first()
    if not jogador:
        return {"message": "Jogador não encontrado"}, 404

    # Atualizar o nome
    jogador.nome = form.novoNome

    try:
        session.commit()
        return jsonify({"message": "Nome do jogador atualizado com sucesso!"}), 200
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao atualizar o nome"}, 400
    
@app.delete('/delete_session', tags=[sessao])
def delete_session(form : SessaoDelet):
    session = Session()

    # Buscar a sessão pelo ID
    sessao = session.query(Sessoes).filter(Sessoes.id == form.idSessao).first()
    if not sessao:
        return {"message": "Sessão não encontrada"}, 404

    try:
        session.delete(sessao)
        session.commit()
        return jsonify({"message": "Sessão apagada com sucesso!"}), 200
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao apagar a sessão"}, 400

