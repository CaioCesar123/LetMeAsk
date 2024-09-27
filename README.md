
# LetMeAsk - Backend

## Descrição

O **LetMeAsk** é um sistema de perguntas e respostas, onde o jogador pode se registrar, alterar seu nome e escolher um tema para responder a perguntas. Este repositório contém o backend da aplicação, desenvolvido em Python com Flask e usando SQLite como banco de dados.

## Tecnologias

- **Python**: Linguagem principal usada no desenvolvimento.
- **Flask**: Framework para desenvolvimento web e API RESTful.
- **SQLite**: Banco de dados relacional para persistência dos dados.
- **Docker**: Para containerização e fácil execução do projeto.

## API Externa: Trivia API
O **LetMeAsk** utiliza uma API externa de Trivia para buscar as perguntas das sessões de jogo. A Trivia API fornece questões com diferentes temas e níveis de dificuldade.

### Detalhes da Trivia API
- **Endpoint**: O endpoint da Trivia API permite a seleção de perguntas filtradas por categoria e dificuldade.
- **Formato de Resposta**: A Trivia API retorna as perguntas em formato JSON, facilitando a integração com o backend.
- **Parâmetros Usados**: No LetMeAsk, usamos parâmetros como `categoria` e `dificuldade` para definir as perguntas de cada sessão.

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/CaioCesar123/LetMeAsk

```

2. Crie um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o servidor:

```bash
flask run
```

## Docker

Você pode rodar o projeto em um container Docker:

1. Construa a imagem Docker:

```bash
docker build -t letmeask .
```

2. Rode o container:

```bash
docker run -p 5000:5000 letmeask
```
