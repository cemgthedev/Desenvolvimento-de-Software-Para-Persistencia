from models.index import Book
from fastapi import APIRouter, HTTPException
import os
import xml.etree.ElementTree as ET
from utils.generate_id import generate_id

router = APIRouter()

# Caminho do arquivo XML
filepath = os.path.join("data", "books.xml")

# Rota para criar um novo livro
@router.post("/books")
async def create_book(book: Book):
    try:        
        # Carregar o XML existente
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Gerando id aleatório
        book.id = generate_id()

        # Criar um novo elemento de livro
        book_element = ET.SubElement(root, "book", id=book.id)
        ET.SubElement(book_element, "title").text = book.title
        ET.SubElement(book_element, "author").text = book.author
        ET.SubElement(book_element, "year").text = str(book.year)
        ET.SubElement(book_element, "genre").text = book.genre

        # Salvar as alterações no arquivo
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        return {"message": "Book created successfully", "data": book}
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get("/books/{id}")
async def get_book(id: str):
    try:
        # Carregar o XML existente
        tree = ET.parse(filepath)
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
            
            return {"book": book_data}
        raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.put("/books/{id}")
async def update_book(id: str, book_update: Book):
    try:
        # Carregar o XML existente
        tree = ET.parse(filepath)
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
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
            return {"message": "Book updated successfully"};
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.delete("/books/{id}")
async def delete_book(id: str):
    try:
        # Carregar o XML existente
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Buscar o livro pelo ID
        book = root.find(f"./book[@id='{id}']")
        if book is not None:
            root.remove(book)
            # Salvar as alterações no arquivo
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
            
            return {"message": "Book deleted successfully"}
        raise HTTPException(status_code=404, detail="Book not found")
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get("/books")
async def get_books():
    try:
        # Carregar o XML existente
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Iterar sobre os elementos de livros e convertê-los em dicionários
        books = []
        for book in root.iter("book"):
            books.append({
                "id": book.attrib.get("id"),
                "title": book.find("title").text,
                "author": book.find("author").text,
                "year": int(book.find("year").text),
                "genre": book.find("genre").text,
            })
        
        return {"books": books}
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing the XML file")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")