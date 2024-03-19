from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""SEMPRE USO OS 3 PARA SETTAR O SELENIUM"""

from selenium.webdriver.chrome.options import Options

"""CONFIG DO NAVEGADOR"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

"""usos"""
import time

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

lista_links = []
paginas = 2
i = 0

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)


def capturarLinks():
    elementos_celulares = WebDriverWait(navegador, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".news-list-item"))
    )
    print(len(elementos_celulares))
    for elemento in elementos_celulares:
        link = elemento.get_attribute("href")
        if link != None:
            print(link)
            lista_links.append(link)


try:
    navegador.get("https://www.tudocelular.com/celulares/provas.html")
    while i <= paginas:
        capturarLinks()
        for _ in range(5):
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        capturarLinks()
        i += 1
    lista_links = list(set(lista_links))  # Remover duplicatas
    with open("lista.txt", "w+") as my_file:
        my_file.write("\n".join(lista_links))

except:
    print("Não encontrei a página")
