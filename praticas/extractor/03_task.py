import requests;
from bs4 import BeautifulSoup;
import pandas as pd;
import os;
import re;
from pdfminer.high_level import extract_text;
import pytesseract;
from PIL import Image;

# buscando dados da página 
baseurl = 'https://github.com/cemgthedev/Desenvolvimento-de-Software-Para-Persistencia';
response = requests.get(baseurl);
site = BeautifulSoup(response.text, 'html.parser');

# capturando o texto do título
titulo = site.title.string;
start_index = titulo.find('/') + 1;
end_index = titulo.find(':');
titulo = titulo[start_index:end_index].lower().strip();

links_directories = site.findAll('a', {'aria-label': re.compile('Directory')});

directories = [];
for directory in links_directories:
    name = directory['aria-label'].split(',')[0].strip();
    url = 'https://github.com' + directory['href'];
    
    # Filtra a lista `directories` para ver se o nome já está presente
    include = list(filter(lambda x: x['name'] == name, directories));
    if len(include) == 0:
        directories.append({
            'name': name,
            'url': url
        });
        
directories_df = pd.DataFrame(directories);

text = extract_text("Plano de Aula.pdf");
text = text.split('\n');

listas = [];

for line in text:
    include = line.find('Lista');
    if include != -1:
        listas.append(line);

lists_df = pd.DataFrame(listas);

# Carregar a imagem
image = Image.open("img.png");

# Extrair texto da imagem
image_text = pytesseract.image_to_string(image);
motivation_df = pd.DataFrame([image_text]);

# Salvando dados em um arquivo excel com sub tabelas quotes e tags
archive_name = titulo + '.xlsx';
os.makedirs('storage', exist_ok=True);
with pd.ExcelWriter('./storage/' + archive_name) as writer:
    directories_df.to_excel(writer, sheet_name="directories", index=False);
    lists_df.to_excel(writer, sheet_name="lists", index=False);
    motivation_df.to_excel(writer, sheet_name="motivation", index=False);