""" 
Teste Tecnico BCP Estágio Analista de Dados 
Gabriel Caruzo Espindola
+    
Processo de automação foi feito via Selenium, onde o código acessa o site da ANBIMA, e faz o download
O processo de tartamento de dados foi feito via Pandas, onde o código lê os arquivos baixados, 
e os trata para que sejam salvos em um arquivo Excel final.
    
Foram utilizadas as bibliotecas: time, os, re, datetime, pandas, matplotlib.pyplot e selenium

As funções foram separadas em 3 partes: automacao, alterar_nome, data_set, adicionar_indexador_debentures e plotar_graficos

Automacao: entra automaticamente no site e pelo calendario pega os ultimo 5 dia  utéis e através de um loop faz o download dos 5 arquivos em xls referente a cada data, chama a variavel download_dir para realizar o salvamento
na pasta Daily Prices, chama a função alterar_nome para a alteração do nome do arquivo baixado.

Alterar_nome: recebe o nome do arquivo baixado em xls no padrão do site, renomeia o arquivo para o formato AAAAMMDD.xls essa informação é retirada do input informado pelo usuário

Data_set: lê os arquivos baixados, faz o tratamento dos dados com o pandas, adicionando coluna data que é retirada diretamente de dentro do arquivo da coluna b linha 4 formatada para aaaa/dd/mm, 
removendo linhas e colunas indesejadas, e por fim salva em um arquivo do dataset unico

Adicionar_indexador_debentures: lê o arquivo do dataset unico, adiciona a coluna Indexador de debentures, que é retirada da coluna Índice/ Correção, e salva no arquivo final

plotar_graficos: lê o arquivo do dataset unico, verifica se as colunas necessárias estão presentes, converte a coluna data para datetime, a coluna Taxa Indicativa para numérico,
agrupa por Indexador de debêntures e data, alem de calcular a média da Taxa Indicativa, e por fim plota um gráfico para cada indexador

"""

#importando as bibliotecas basicas
import time
import os
import re
from datetime import datetime



# Bibliotecas manipulação de dados
import pandas as pd
import matplotlib.pyplot as plt

#importando as bibliotecas do selenium/arquivo de automação
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#importando a biblioteca tkinter para a interface visual
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

# Caminhos dos diretórios e arquivos (ajustar para o seu ambiente)
driver_path = 'C:/Users/gabri/OneDrive/Área de Trabalho/Desafio BCP/chromedriver-win64/chromedriver-win64/chromedriver.exe'
download_dir = 'C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Desafio BCP\\Daily Prices'
Caminho_Final = os.path.join(download_dir, 'dataset_final.xlsx')

# Configurando as preferências do Chrome para definir o diretório de download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_dir}
chrome_options.add_experimental_option('prefs', prefs)

# Inicializando o WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL do site da ANBIMA
url = 'https://www.anbima.com.br/informacoes/merc-sec-debentures/default.asp'

def Automacao():
    # Pega os ultimos 5 dias uteis baseado na data atual(Do computador)
    datas = pd.date_range(end=datetime.today(), periods=7, freq='B').strftime('%d/%m/%Y').tolist()
    num_repeticoes = 5

    for i in range(num_repeticoes):
        try:
            data_input = datas[i]
            driver.get(url)
            campo_data = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'Dt_Ref'))
            )
            campo_data.clear()
            campo_data.send_keys(data_input)
            botao_consulta = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'Consultar'))
            )
            botao_consulta.click()
            time.sleep(5)
            inicio_download = set(os.listdir(download_dir))
            botao_download = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, ".xls") and contains(@class, "linkinterno")]'))
            )
            update_status("Arquivo encontrado para download.")
            botao_download.click()
            time.sleep(5)
            final_download = set(os.listdir(download_dir))
            novo_arquivo = final_download - inicio_download
            if novo_arquivo:
                downloaded_nome = novo_arquivo.pop()
                update_status(f"Arquivo baixado: {downloaded_nome}")
                Alterar_nome(downloaded_nome, datas, i)
            else:
                update_status("Nenhum novo arquivo foi baixado.")
            time.sleep(1)
        except Exception as e:
            update_status(f"Algo deu errado no download: {e}")

    driver.quit()
    data_set(datas)
    adicionar_indexador_debentures(Caminho_Final)  # Chama a função do Indexador de Debêntures


# Função para alterar o nome do arquivo baixado
def Alterar_nome(downloaded_filename, datas, index):
    data_input = datas[index]
    dia, mes, ano = data_input.split('/')
    new_filename = f'{ano}{mes}{dia}.xls'
    new_filepath = os.path.join(download_dir, new_filename)
    downloaded_filepath = os.path.join(download_dir, downloaded_filename)
    while not os.path.exists(downloaded_filepath):
        time.sleep(1)
    while True:
        try:
            os.rename(downloaded_filepath, new_filepath)
            update_status(f"Arquivo renomeado para: {new_filename}")
            break
        except PermissionError:
            time.sleep(1)

# Função para tratar os dados e salvar em um arquivo final do dataset
def data_set(datas):
    all_data = []
    for data_input in datas:
        dia, mes, ano = data_input.split('/')
        filename = f'{ano}{mes}{dia}.xls'
        filepath = os.path.join(download_dir, filename)
        if os.path.exists(filepath):
            xls = pd.ExcelFile(filepath)
            for sheet_name in xls.sheet_names:
                df_colunas = pd.read_excel(xls, sheet_name=sheet_name, skiprows=7, nrows=2)
                column_names = df_colunas.columns.tolist()
                df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=9, header=None)
                df.columns = column_names
                df = df.dropna(axis=1, how='all')
                df = df.dropna(subset=['Código'])
                data_value = pd.read_excel(xls, sheet_name=sheet_name, skiprows=3, nrows=1, usecols='B', header=None).iloc[0, 0]
                if pd.isna(data_value):
                    update_status(f"Valor da data na linha 4, coluna B está vazio na aba {sheet_name} do arquivo {filename}.")
                else:
                    data_value = pd.to_datetime(data_value).strftime('%d/%m/%Y')
                    df['data'] = data_value
                strings_para_remover = ['cláusula', 'negociação', 'divulgados']
                pattern = '|'.join(strings_para_remover)
                if 'Código' in df.columns:
                    df = df[~df['Código'].str.contains(pattern, na=False)]
                else:
                    update_status(f"A coluna 'Código' não foi encontrada na aba {sheet_name} do arquivo {filename}.")
                all_data.append(df)
    final_df = pd.concat(all_data, ignore_index=True)
    with pd.ExcelWriter(Caminho_Final) as writer:
        final_df.to_excel(writer, sheet_name='Consolidado', index=False)
    update_status(f"Todos os dados foram salvos na aba 'Consolidado' do arquivo {Caminho_Final}.")


# Função para adicionar a coluna Indexador de Debêntures ao arquivo final
def adicionar_indexador_debentures(filepath):
    df = pd.read_excel(filepath, sheet_name='Consolidado')
    if 'Índice/ Correção' in df.columns:
        def clean_indexador(value):
            if pd.isna(value):
                return None
            match = re.search(r'(IPCA \+|DI \+|do DI)', value)
            return match.group(0) if match else None
        df['Indexador de debêntures'] = df['Índice/ Correção'].apply(clean_indexador)
        cols = [df.columns[0], 'Indexador de debêntures'] + [col for col in df.columns if col not in ['Indexador de debêntures', df.columns[0]]]
        df = df[cols]
    else:
        update_status("A coluna 'Índice/ Correção' não foi encontrada no DataFrame final.")
    df.to_excel(filepath, sheet_name='Consolidado', index=False)
    update_status(f"A coluna 'Indexador de debêntures' foi adicionada ao arquivo {filepath}.")



def iniciar_automacao():
    Automacao()
    messagebox.showinfo("Informação", f"Automação concluída em {datetime.now().strftime('%d/%m/%Y')}")

def adicionar_indexador():
    adicionar_indexador_debentures(Caminho_Final)
    messagebox.showinfo("Informação", "Indexador de debêntures adicionado!")

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()


""" Criação de uma intrface visual para a execução das automação"""
# Janela principal
root = tk.Tk()
root.title("Automação de Dados - BCP")
root.configure(bg="darkblue")

# Carregar a imagem da logo
logo_path = "C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Desafio BCP\\logo_transparente.png"  
logo_image = Image.open(logo_path)

# Adicionar fundo da cor da root à imagem
bg_color = root.cget("bg")
logo_image_with_bg = Image.new("RGBA", logo_image.size, bg_color)
logo_image_with_bg.paste(logo_image, (0, 0), logo_image)

# Melhorar a resolução da imagem ao redimensioná-la
logo_image_with_bg = logo_image_with_bg.resize((273, 106), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image_with_bg)

# Ajustar a geometria da janela principal com base na resolução da imagem
window_width = 300
window_height = 400 + logo_image_with_bg.height
root.geometry(f"{window_width}x{window_height}")


# Imagem da logo à janela
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=20)

# Exibir a data atual
data_label = tk.Label(root, text=f"Data: {datetime.now().strftime('%d/%m/%Y')}")
data_label.pack(pady=10)

# Exibir o status da automação
status_label = tk.Label(root, text="Status: Realizando Download...")
status_label.pack(pady=10)

# Botões para as funcionalidades
btn_automacao = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
btn_automacao.pack(pady=10)


# Execução da janela principal
root.mainloop()