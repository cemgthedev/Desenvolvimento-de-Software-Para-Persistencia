import pickle

# Exemplo de objeto a ser serializado
dados = {"nome": "Alice", "idade": 25, "cursos": ["Python", "Data Science"]}

# Serializar o objeto e salvar em um arquivo
with open("dados.pkl", "wb") as file:
    pickle.dump(dados, file)
    
with open("dados.pkl", "rb") as file:
    dados = pickle.load(file)
    
print(f"Nome: {dados['nome']}\nIdade: {dados['idade']}\nCursos: {dados['cursos']}\n");