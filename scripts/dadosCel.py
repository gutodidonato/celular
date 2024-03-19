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

import time

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

import openpyxl

wb = openpyxl.Workbook()
planilha = wb.active
# Adicionar cabeçalhos
planilha.append(["Nome", "Custo/Benefício", "Hardware", "Tela", "Câmera", "Desempenho"])


def correcaoString(string_comum):
    if string_comum[:3].endswith("/"):
        return string_comum[:1]
    else:
        return string_comum[:3]


servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

with open("lista.txt", "r") as f:
    for linha in f:
        try:
            print(linha)
            navegador.get(linha.strip())
            dados_tecnicos = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".lista_cursor li a"))
            )
            dados_tecnicos.click()
            """guia de dados"""

            nome = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="fwide_column"]/h2'))
            )

            print(nome.text)

            custoBeneficio = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="phone_columns"]/div/ul[3]/li[1]/b')
                )
            )

            print(custoBeneficio.text)

            hardware = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="phone_columns"]/div/ul[3]/li[2]/b')
                )
            )

            print(hardware.text)

            tela = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="phone_columns"]/div/ul[3]/li[3]')
                )
            )

            print(tela.text)

            camera = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="phone_columns"]/div/ul[3]/li[4]')
                )
            )
            print(camera.text)

            desempenho = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="phone_columns"]/div/ul[3]/li[5]')
                )
            )
            tela = correcaoString(tela.text)
            camera = correcaoString(camera.text)
            desempenho = correcaoString(desempenho.text)
            print(
                f"{nome.text}, {custoBeneficio.text}, {hardware.text}, {tela}, {camera}, {desempenho}"
            )

            try:
                planilha.append(
                    [
                        nome.text,
                        custoBeneficio.text,
                        hardware.text,
                        tela,
                        camera,
                        desempenho,
                    ]
                )
            except:
                print("Falha no wookbook")
        except:
            pass
            print("Não achei")
            time.sleep(2)
    wb.save("dados_celulares.xlsx")
    navegador.quit()
