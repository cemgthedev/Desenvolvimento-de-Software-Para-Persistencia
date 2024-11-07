import json

# Leitura do arquivo JSON
with open("dados.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Exemplo de acesso aos dados
print(data["clientes"]);

# Escreve os dados com tabulações
print(json.dumps(data, indent=4, ensure_ascii=False))