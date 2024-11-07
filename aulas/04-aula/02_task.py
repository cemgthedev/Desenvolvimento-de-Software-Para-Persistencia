import pdfplumber

with pdfplumber.open("Relatorio_anual_dados.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
