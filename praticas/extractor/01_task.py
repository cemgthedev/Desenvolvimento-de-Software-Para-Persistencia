import requests;
from bs4 import BeautifulSoup;
import pandas as pd;
import os;

# buscando dados da página 
baseurl = 'https://quotes.toscrape.com';
response = requests.get(baseurl);
site = BeautifulSoup(response.text, 'html.parser');

# capturando o texto do título
titulo = site.title.string;

# capturando dados de autores, citações e tags
quotes = [];
for quote in site.findAll('div', {'class': 'quote'}):
    
    # capturando textos de autor, citação e tags
    author = quote.find('small', {'class': 'author'});
    citation = quote.find('span', {'class': 'text'});
    tags = quote.findAll('a', {'class': 'tag'});
    
    # adicionando dados em uma lista de citações
    quotes.append({
        'author': author.string,
        'citation': citation.string,
        'tags': [tag.string for tag in tags]
    });

# capturando tags e seus links
tags = [];
for tag in site.findAll('a', {'class': 'tag'}):
    tags.append({
        'tag': tag.string,
        'link': baseurl + tag.get('href')
    });

# Criando data frames das citações e tags
quotes_df = pd.DataFrame(quotes);
tags_df = pd.DataFrame(tags);

# Salvando dados em um arquivo excel com sub tabelas quotes e tags
archive_name = titulo.replace(' ', '-').lower() + '.xlsx';
os.makedirs('storage', exist_ok=True);
with pd.ExcelWriter('./storage/' + archive_name) as writer:
    quotes_df.to_excel(writer, sheet_name="quotes", index=False);
    tags_df.to_excel(writer, sheet_name="tags", index=False);