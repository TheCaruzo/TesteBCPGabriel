""" 
Teste Tecnico BCP Estágio Analista de Dados 
Gabriel Caruzo Espindola
    
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
from PIL import Image, ImageTk

# Caminhos dos diretórios e arquivos (ajustar para o seu ambiente)
driver_path = 'C:/Users/gabri/OneDrive/Área de Trabalho/Desafio BCP/chromedriver-win64/chromedriver-win64/chromedriver.exe'
download_dir = 'C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Desafio BCP\\Daily Prices'
final_filepath = os.path.join(download_dir, 'dataset_final.xlsx')

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
    datas = pd.date_range(end=datetime.today(), periods=7, freq='B').strftime('%d/%m/%Y').tolist()[-6:]
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
            before_download = set(os.listdir(download_dir))
            botao_download = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, ".xls") and contains(@class, "linkinterno")]'))
            )
            update_status("Arquivo encontrado para download.")
            botao_download.click()
            time.sleep(5)
            after_download = set(os.listdir(download_dir))
            new_files = after_download - before_download
            if new_files:
                downloaded_filename = new_files.pop()
                update_status(f"Arquivo baixado: {downloaded_filename}")
                Alterar_nome(downloaded_filename, datas, i)
            else:
                update_status("Nenhum novo arquivo foi baixado.")
            time.sleep(1)
        except Exception as e:
            update_status(f"Algo deu errado no download: {e}")

    driver.quit()
    data_set(datas)

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

def data_set(datas):
    all_data = []
    for data_input in datas:
        dia, mes, ano = data_input.split('/')
        filename = f'{ano}{mes}{dia}.xls'
        filepath = os.path.join(download_dir, filename)
        if os.path.exists(filepath):
            xls = pd.ExcelFile(filepath)
            for sheet_name in xls.sheet_names:
                df_columns = pd.read_excel(xls, sheet_name=sheet_name, skiprows=7, nrows=2)
                column_names = df_columns.columns.tolist()
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
    with pd.ExcelWriter(final_filepath) as writer:
        final_df.to_excel(writer, sheet_name='Consolidado', index=False)
    update_status(f"Todos os dados foram salvos na aba 'Consolidado' do arquivo {final_filepath}.")

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

def plotar_graficos(filepath):
    df = pd.read_excel(filepath, sheet_name='Consolidado')
    required_columns = ['data', 'Indexador de debêntures', 'Taxa Indicativa']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        update_status(f"As seguintes colunas necessárias não foram encontradas no DataFrame: {', '.join(missing_columns)}")
        return
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['Taxa Indicativa'] = pd.to_numeric(df['Taxa Indicativa'], errors='coerce')
    df_grouped = df.groupby(['Indexador de debêntures', 'data'])['Taxa Indicativa'].mean().reset_index()
    indexadores = df_grouped['Indexador de debêntures'].unique()
    for indexador in indexadores:
        df_indexador = df_grouped[df_grouped['Indexador de debêntures'] == indexador]
        plt.figure(figsize=(10, 6))
        plt.plot(df_indexador['data'], df_indexador['Taxa Indicativa'], marker='o')
        plt.title(f'Taxa Indicativa por Data - {indexador}')
        plt.xlabel('Data')
        plt.ylabel('Taxa Indicativa')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


""" Criação de uma intrface visual para a execução das automação"""
def iniciar_automacao():
    Automacao()
    messagebox.showinfo("Informação", f"Automação concluída em {datetime.now().strftime('%d/%m/%Y')}")


def plotar_graficos_interface():
    plotar_graficos(final_filepath)
    messagebox.showinfo("Informação", "Gráficos plotados!")

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()


# Janela principal
root = tk.Tk()
root.title("Automação de Dados - BCP")
root.geometry("800x600") 
root.configure(bg="darkblue")

# Carregar a imagem da logo
logo_path = "C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Desafio BCP\\logo-black-.png"  
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((200, 200), Image.LANCZOS)  
logo_photo = ImageTk.PhotoImage(logo_image)

# Imagem da logo à janela
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=20)

# Exibir a data atual
data_label = tk.Label(root, text=f"Data: {datetime.now().strftime('%d/%m/%Y')}")
data_label.pack(pady=10)

# Exibir o status da automação
status_label = tk.Label(root, text="Status: Aguardando...")
status_label.pack(pady=10)

# Botões para as funcionalidades
btn_automacao = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
btn_automacao.pack(pady=10)

btn_plotar_graficos = tk.Button(root, text="Plotar Gráficos", command=plotar_graficos_interface)
btn_plotar_graficos.pack(pady=10)

# Execução da janela principal
root.mainloop()