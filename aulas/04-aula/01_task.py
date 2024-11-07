import requests
from bs4 import BeautifulSoup

# buscando dados da página 
link = 'https://quotes.toscrape.com/';
response = requests.get(link);
site = BeautifulSoup(response.text, 'html.parser');

# capturando o texto do título
titulo = site.title.string;

# capturando as citações
quotes = [];
for quote in site.findAll('div', {'class': 'quote'}):
    
    # capturando textos de autor, citação e tags
    author = quote.find('small', {'class': 'author'});
    text = quote.find('span', {'class': 'text'});
    tags = quote.findAll('a', {'class': 'tag'});
    
    # adicionando dados em uma lista de citações
    quotes.append({
        'author': author.string,
        'text': text.string,
        'tags': [tag.string for tag in tags]
    });

print(titulo);
print(quotes);