import zipfile
import os

# Listando arquivos do diretório 'arquivos'
path = './arquivos'
found_archives = os.listdir(path);
print(f"Arquivos encontrados: {found_archives}\n");

archives = [];
while True:
    opcao = input('1 - Adicionar arquivo;\n2 - Adicionar todos os arquivos;\n3 - Finalizar operação.\nSelecione uma opção: ');
    if opcao == '1':
        file_name = input('Digite o nome do arquivo: ');
        archives.append(file_name);
    elif opcao == '2':
        archives = found_archives;
        break;
    elif opcao == '3':
        break;
        

# Implementando uma função que conta o número de linhas, caracteres e palavras de um arquivo
def info(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        words = 0
        characters = 0
        for line in lines:
            words += len(line.split())
            characters += len(line)
        return {
            "name": file_name,
            "n_lines": len(lines), 
            "n_words": words, 
            "n_characters": characters
        }

# Implementando uma função que remove linhas em branco
def remove_blank_lines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    with open(file_name, 'w') as file:
        for line in lines:
            if line.strip():
                file.write(line)

# Criando o arquivo 'consolidado.txt' em modo de escrita
with open('consolidado.txt', 'w') as file:
    file.write('caminho do arquivo; número de linhas; número de palavras; número de caracteres\n');
    
    for file_name in archives:
        archive = path + '/' + file_name;
        
        try:
            # Removendo linhas em branco
            remove_blank_lines(archive);
            
            # Contando o número de linhas, palavras e caracteres e escrevendo no arquivo
            infos = info(archive);
            file.write(f'{infos["name"]}; {infos["n_lines"]}; {infos["n_words"]}; {infos["n_characters"]}\n');
        except FileNotFoundError:
            print(f'Arquivo {file_name} não encontrado\n');
            break;

# Criando o arquivo .zip
zip = 'saida.zip';
with zipfile.ZipFile(zip, 'w') as z:
    z.write('consolidado.txt');