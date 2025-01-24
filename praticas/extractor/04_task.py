from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurar o WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar o navegador em modo headless (opcional)
chrome_driver_path = "/caminho/para/seu/chromedriver"  # Altere para o caminho do seu WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL da página
url = 'https://www.lightnovelworld.com/novel/scholars-advanced-technological-system-466/chapter-1'

# Abrir a página
driver.get(url)

# Esperar a página carregar (ajuste o tempo conforme necessário)
time.sleep(5)

# Capturar o conteúdo desejado
try:
    content = driver.find_element(By.CLASS_NAME, "main-content")
    print(content.text)
except Exception as e:
    print("Erro ao capturar o conteúdo:", e)

# Fechar o navegador
driver.quit()