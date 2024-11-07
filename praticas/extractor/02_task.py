import pytesseract;
from PIL import Image;

# Carregar a imagem
image = Image.open("img.png");

# Extrair texto da imagem
text = pytesseract.image_to_string(image);

with open("image-text.txt", "w") as file:
    file.write(text);
    
# Link do Google Colab
# https://colab.research.google.com/drive/1hdqtnfmPtfxdnzYcwjQ2lTw0hSkrDjnK?usp=sharing