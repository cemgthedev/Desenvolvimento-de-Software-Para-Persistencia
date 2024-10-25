def ler_arquivo():
    with open('arquivo.txt', 'r', encoding='utf-8') as file:
        print(file.read())

def ler_linha_arquivo():
    with open('arquivo.txt', 'r', encoding='utf-8') as file:
        print(file.readline())

def ler_linha_por_linha_arquivo():
    with open('arquivo.txt', 'r', encoding='utf-8') as file:
        contador = 1
        for line in file:
            print("Linha ", contador, ":", contador, line)
            contador += 1

def ler_arquivo_bom():
    with open('arquivo_bom.txt', 'r', encoding='utf-8-sig') as file:
        print(file.read())

def escrever_arquivo(string):
    with open('arquivo.txt', 'w') as file:
        file.write(string)
        
while(True):
    opcao = input('1 - Ler arquivo\n2 - Ler arquivo BOM (Byte Order Mark)\n3 - Ler linha do arquivo\n4 - Ler linha por linha do arquivo\n5 - Escrever\n6 - Sair\nSelecione uma opção: ')
    if opcao == '1':
        ler_arquivo()
    elif opcao == '2':
        ler_arquivo_bom()
    elif opcao == '3':
        ler_linha_arquivo()
    elif opcao == '4':
        ler_linha_por_linha_arquivo()
    elif opcao == '5':
        string = input('Digite a string: ')
        escrever_arquivo(string)
    elif opcao == '6':
        break

