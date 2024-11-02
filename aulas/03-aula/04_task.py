import zipfile

# Caminho do arquivo que será lido
path = './arquivo.zip'

# Lendo o arquivo
with zipfile.ZipFile(path, 'r') as zip_ref:
    # Percorrendo os arquivos dentro do .zip
    for file_name in zip_ref.namelist():
        # Lendo cada arquivo dentro do .zip
        with zip_ref.open(file_name) as file:
            # Imprimindo cada linha do arquivo
            for line in file:
                print(line.strip());
            