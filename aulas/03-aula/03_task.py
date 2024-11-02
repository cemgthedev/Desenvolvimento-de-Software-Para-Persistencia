import zipfile

# Arquivo que será criado
nome_arquivo_zip = 'arquivo.zip'

# Arquivos para incluir no zip
arquivos_para_zipar = ['arquivo.txt', 'veiculos.csv']

# Criando o arquivo zip
with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
    for arquivo in arquivos_para_zipar:
        zipf.write(arquivo)