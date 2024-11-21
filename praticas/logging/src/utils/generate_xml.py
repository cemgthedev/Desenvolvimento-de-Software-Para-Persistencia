import os
import xml.etree.ElementTree as ET

def generate_xml():
    # Diretório e nome do arquivo
    directory = "data"
    filename = "books.xml"

    # Criar o diretório, se não existir
    os.makedirs(directory, exist_ok=True)

    # Caminho completo para o arquivo
    filepath = os.path.join(directory, filename)

    # Verificar se o arquivo XML existe
    if not os.path.exists(filepath):
        # Criar a estrutura básica do XML
        root = ET.Element("books")
        tree = ET.ElementTree(root)

        # Salvar o arquivo
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        print(f"Arquivo '{filename}' criado em '{directory}'.")

    # Carregar o arquivo XML
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        print(f"Arquivo '{filename}' carregado com sucesso.")
    except ET.ParseError as e:
        print(f"Erro ao carregar o arquivo XML: {e}")