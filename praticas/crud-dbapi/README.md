# Executando

- Criar um ambiente virtual com o seguinte comando: python -m venv .venv
- Rodar ambiente no prompt de comando do windows: .venv\Scripts\activate
- Instalar libs: pip install fastapi uvicorn psycopg2
- Entrar na pasta src: cd src
- Executar o servidor com o seguinte comando: uvicorn main:app --reload