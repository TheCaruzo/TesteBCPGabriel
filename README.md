# TesteTecnicobcp
Teste técnico BCP - Gabriel Caruzo Espindola

# Automação de Download e Análise de Dados

Este projeto automatiza o download de dados e a geração de gráficos utilizando Selenium e Pandas.

## Descrição

Este script utiliza Selenium para automatizar o navegador Google Chrome, baixar arquivos de dados e processá-los utilizando Pandas. E também utiliza tkinker e PIL
## Instalação

### Pré-requisitos
- Python 3.x
- Google Chrome
- ChromeDriver compatível com a versão do seu Google Chrome

### Bibliotecas Python
- time: Para manipulação de tempo e pausas na execução do script.
- os: Para manipulação de caminhos de diretórios e arquivos.
- re: Para operações com expressões regulares.
- datetime: Para manipulação de datas e horas.
- pandas: Para manipulação e análise de dados.
- selenium: Para automação de navegadores web.
- tkinter: Para exibir caixas de mensagem na interface gráfica.
- PIL: Para manipular e exibir imagens na interface gráfica.

### PIP Install
- pip install 
- pip pandas 
- pip matplotlib 
- pip selenium
- pip tkinter

### Funções Automação

### automacao()
**Descrição:** Esta função automatiza o processo de acesso ao site da ANBIMA, obtém os últimos 5 dias úteis e faz o download dos arquivos XLS correspondentes a cada data. 

**Variáveis:**
- `datas`: Lista que contém os últimos 5 dias úteis.
- `num_repeticoes`: Número de vezes que o processo será repetido, usado em um loop.
- `data_input`: Lista gerada a partir da variável `datas`.
- `driver.get`: Acessa a URL do site.
- `campo_data`: Caminho do campo para informar a data.
- `botao_consulta`: Caminho do botão de consulta.


Utiliza Selenium para automação do navegador. Chama a função `alterar_nome` para renomear os arquivos baixados.

Os arquivos são salvos no diretório especificado por `download_dir`. Utiliza Selenium para automação do navegador. Chama a função `alterar_nome` para renomear os arquivos baixados.
 
### alterar_nome(nome_arquivo)
**Descrição:** Esta função renomeia o arquivo baixado no formato padrão do site para o formato AAAAMMDD.xls, onde a data é retirada do input informado pelo usuário.

- `download_dir`: Lista que contém os últimos 5 dias úteis.
- `num_repeticoes`: Número de vezes que o processo será repetido, usado em um loop.
- `data_input`: Lista gerada a partir da variável `datas`.
- `driver.get`: Acessa a URL do site.
- `campo_data`: Caminho do campo para informar a data.
- `botao_consulta`: Caminho do botão de consulta.


### data_set()
**Descrição:** Esta função lê os arquivos baixados, faz o tratamento dos dados com o pandas, adicionando a coluna data que é retirada diretamente de dentro do arquivo da coluna B linha 4 formatada para AAAA/DD/MM, removendo linhas e colunas indesejadas, e por fim salva em um arquivo do dataset único.

- `all_data`: Lista que armazena todos os DataFrames lidos.
- `final_df`: DataFrame final concatenado.
- `Caminho_Final`: Caminho do arquivo final onde os dados tratados serão salvos.

### adicionar_indexador_debentures(filepath)
**Descrição:** Esta função lê o arquivo do dataset único, adiciona a coluna "Indexador de debêntures", que é retirada da coluna "Índice/ Correção", e salva no arquivo final.
- `df`: DataFrame lido do arquivo Excel.
- `clean_indexador`: Função interna que limpa e extrai o indexador da coluna "Índice/ Correção".
- `cols`: Lista de colunas reorganizadas para incluir "Indexador de debêntures".


### iniciar_automacao()
**Descrição:** Esta função inicia o processo de automação chamando a função automacao e exibe uma mensagem informando a conclusão.

### adicionar_indexador()
**Descrição:** Esta função chama a função adicionar_indexador_debentures e exibe uma mensagem informando a adição do indexador.

### update_status(message)
**Descrição:** Esta função atualiza o status exibido na interface gráfica com a mensagem fornecida.


### Interface Gráfica
**Descrição:** A interface gráfica é criada usando a biblioteca tkinter. Inclui a exibição de uma imagem de logo, a data atual, o status da automação e botões para iniciar a automação e adicionar o indexador.

- `root`: Janela principal da interface gráfica.
- `logo_path`: Caminho da imagem da logo.
- `logo_image`: Imagem da logo redimensionada.
- `logo_photo`: Foto da logo para exibição na interface.
- `logo_label`: Label que exibe a imagem da logo.
- `data_label`: Label que exibe a data atual.
- `status_label`: Label que exibe o status da automação.
- `btn_automacao`: Botão para iniciar a automação.


![image](https://github.com/user-attachments/assets/a8927412-6db3-475e-95a1-acfded6a6396)


### Power BI
Foi tratado os dados e deixando somente as counas Código, Nome, Preço e Taxas Negociadas. Com isso foi gerado os grafícos solicitados 

**Media Taxa Indicativa por data**


![image](https://github.com/user-attachments/assets/62d2a7b5-94da-49cc-bdde-2cbb41e1b4bd)



**Media Taxa Indicativa DI+**



![image](https://github.com/user-attachments/assets/6455e569-276d-4ca2-9a52-cb9981f109eb)



**Media Taxa Indicativa  IPCA +**



