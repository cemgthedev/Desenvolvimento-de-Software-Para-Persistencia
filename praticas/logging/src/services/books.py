from fastapi import APIRouter, HTTPException
import os
import xml.etree.ElementTree as ET
import logging
import yaml
from models.index import Book
from utils.generate_id import generate_id

# Carregar configurações do arquivo YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Configurar o sistema de logging
log_file = config['logging']['file']
log_level = config['logging']['level']
log_format = config['logging']['format']

# Criar o diretório para o arquivo de log, se necessário
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format=log_format,
    filename=log_file,
    filemode='a'
)

logger = logging.getLogger("app_logger")

# Obter o caminho do arquivo XML
data_file = config['data']['file']
xml_filepath = os.path.join("data", "books.xml")

router = APIRouter()

@router.post("/books")
async def create_book(book: Book):
    try:
        logger.info("Tentativa de criar um novo livro.")
        # Carregar o XML existente
        tree = ET.parse(xml_filepath)
        root = tree.getroot()

        # Gerar id único
        book.id = generate_id()

        # Criar um novo elemento no XML
        book_element = ET.SubElement(root, "book", id=book.id)
        ET.SubElement(book_element, "title").text = book.title
        ET.SubElement(book_element, "author").text = book.author
        ET.SubElement(book_element, "year").text = str(book.year)
        ET.SubElement(book_element, "genre").text = book.genre

        # Salvar alterações
        tree.write(xml_filepath, encoding="utf-8", xml_declaration=True)
        logger.info(f"Livro criado com sucesso: {book.title} ({book.id})")
        return {"message": "Book created successfully", "data": book}
    except ET.ParseError as e:
        logger.error(f"Erro ao processar XML: {e}")
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError as e:
        logger.error(f"Arquivo XML não encontrado: {e}")
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao criar livro: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/books/{id}")
async def get_book(id: str):
    try:
        logger.info("Buscando livro pelo ID.")
        # Carregar o XML existente
        tree = ET.parse(xml_filepath)
        root = tree.getroot()
        
        # Buscar o livro pelo ID
        book = root.find(f"./book[@id='{id}']")
        if book is not None:
            book_data = {
                "id": book.attrib.get("id"),
                "title": book.find("title").text,
                "author": book.find("author").text,
                "year": int(book.find("year").text),
                "genre": book.find("genre").text,
            }
            
            logger.info("O livro foi encontrado.")
            return {"book": book_data}
        raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        logger.error("Erro ao processar XML.")
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        logger.error("Arquivo XML não encontrado.")
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar livro: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.put("/books/{id}")
async def update_book(id: str, book_update: Book):
    try:
        logger.info("Atualizando livro.")
        # Carregar o XML existente
        tree = ET.parse(xml_filepath)
        root = tree.getroot()
        
        # Buscar o livro pelo ID
        book = root.find(f"./book[@id='{id}']")
        if book is not None:
            # Atualizar os campos do livro
            book.find("title").text = book_update.title
            book.find("author").text = book_update.author
            book.find("year").text = str(book_update.year)
            book.find("genre").text = book_update.genre

           # Salvar as alterações no arquivo
            tree.write(xml_filepath, encoding="utf-8", xml_declaration=True)
            
            logger.info("Livro atualizado com sucesso.")
            return {"message": "Book updated successfully"};
        else:
            logger.info("Livro nao encontrado.")
            raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        logger.error("Erro ao processar XML.")
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        logger.error("Arquivo XML não encontrado.")
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar livro: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.delete("/books/{id}")
async def delete_book(id: str):
    try:
        logger.info("Deletando livro.")
        # Carregar o XML existente
        tree = ET.parse(xml_filepath)
        root = tree.getroot()
        
        # Buscar o livro pelo ID
        book = root.find(f"./book[@id='{id}']")
        if book is not None:
            root.remove(book)
            # Salvar as alterações no arquivo
            tree.write(xml_filepath, encoding="utf-8", xml_declaration=True)
            
            logger.info("Livro deletado com sucesso.")
            return {"message": "Book deleted successfully"}
        else:
            logger.info("Livro nao encontrado.")
            raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        logger.error("Erro ao processar XML.")
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        logger.error("Arquivo XML não encontrado.")
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao deletar livro: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    
@router.get("/books")
async def get_books():
    try:
        logger.info("Listando todos os livros.")
        # Carregar o XML existente
        tree = ET.parse(xml_filepath)
        root = tree.getroot()

        # Iterar sobre os livros no XML
        books = []
        for book in root.iter("book"):
            books.append({
                "id": book.attrib.get("id"),
                "title": book.find("title").text,
                "author": book.find("author").text,
                "year": int(book.find("year").text),
                "genre": book.find("genre").text,
            })

        logger.info(f"Encontrados {len(books)} livros.")
        return {"books": books}
    except ET.ParseError as e:
        logger.error(f"Erro ao processar XML: {e}")
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError as e:
        logger.error(f"Arquivo XML não encontrado: {e}")
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao listar livros: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/logs/books")
async def get_logs():
    try:
        logger.info("Lendo o arquivo de log.")
        with open(log_file, "r") as f:
            logs = f.read()
            
        logs = logs.split("\n")
        return {"logs": logs}
    except FileNotFoundError as e:
        logger.error(f"Arquivo de log não encontrado: {e}")
        raise HTTPException(status_code=500, detail="Log file not found")
    except Exception as e:
        logger.error(f"Erro inesperado ao acessar logs: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")