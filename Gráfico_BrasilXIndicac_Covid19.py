from typing import final
import requests as r
import csv
import datetime as dt
from PIL import Image
from  IPython.display import display
from requests.api import options

# Função responsável por preparar os dados do brasil
def dados_brasil():
    url = 'https://api.covid19api.com/dayone/country/brazil'
    resp = r.get(url)

    raw_data = resp.json()


    final_data_brasil = [] #Filtrando os dados, iremos guardar apenas os dados desejados 
    for obs in raw_data:
        final_data_brasil.append([obs['Confirmed'], obs['Date']]) # Colocando esses valores em uma lista

    final_data_brasil.insert(0, ['Confrimados', 'data']) # Criando o Headline da lista

    for i in range(1, len(final_data_brasil)):
        final_data_brasil[i][1] = final_data_brasil[i][1][:10] #Manipulando a Data para excluir os caractres depois do 10º caractere 
  
    # Convertendo a Data de string para Data
    for i in range(1, len(final_data_brasil)):
        final_data_brasil[i][1] = dt.datetime.strptime(final_data_brasil[i][1], '%Y-%m-%d' ) 

    return final_data_brasil

def dados_india():
    url = 'https://api.covid19api.com/dayone/country/India'
    resp = r.get(url)

    raw_data = resp.json()


    final_data_india = [] #Filtrando os dados, iremos guardar apenas os dados desejados 
    for obs in raw_data:
        final_data_india.append([obs['Confirmed'], obs['Date']]) # Colocando esses valores em uma lista

    final_data_india.insert(0, ['Confrimados', 'data']) # Criando o Headline da lista


    for i in range(1, len(final_data_india)):
        final_data_india[i][1] = final_data_india[i][1][:10] #Manipulando a Data para excluir os caractres depois do 10º caractere 
   
    # Convertendo a Data de string para Data
    for i in range(1, len(final_data_india)):
        final_data_india[i][1] = dt.datetime.strptime(final_data_india[i][1], '%Y-%m-%d' ) 

    return final_data_india

# Chamando as funções e guardando os dados nas variáveis 
lista_brasil = dados_brasil() 
lista_india = dados_india()


# Formação do gráfico

#Atribuindo os labels e os dados de y
def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label' : labels[i],
                'data' : y[i]
            })
        return datasets
    else:
        return [
            {
                'label' : labels,
                'data' : y
            }
        ]

# Função que verifica se o gráfico tem titulo ou não
def set_title(title=''):
    if title != '':
        display = 'true' # Padrão da API
    else:
        display = 'false'
    return{
        'title' : title,
        'display' : display
    } 

# Juntando todas as informações que compoem o gráfico
def create_chart(x, y, labels, kind='bar', title=''):

        datasets = get_datasets(y, labels) 
        options = set_title(title)

        chart = {
            'type': kind,
            'data' : {
                'labels' : x,
                'datasets' : datasets
            },
            'options': options
        }

        return chart

#Geração do gráfico
def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

#Salvando a imagem do gráfico
def salve_image(path, content):
    with open(path, 'wb') as imagem:
        imagem.write(content)

# Mostrando o gráfico na IDE
def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# Atribuindo os dados de Brasil e india aos valores do gráfico
y_data_1 = []

for obs in lista_brasil[1::30]:
    y_data_1.append(obs[0]) # Adicionando ao eixo Y do gráfico os infecatdos do Brasil

y_data_2 = []

for obs in lista_india[1::30]:
    y_data_2.append(obs[0]) # Adicionando ao eixo Y do gráfico os infecatdos da India

labels = ['Infectados Brasil', 'Infectados India'] # Colunas do gráfico

x_data_1 = []
for obs in lista_brasil[1::30]:
    x_data_1.append(obs[1].strftime('%d/%m/%Y')) # Adciando ao eixo X do gráfico o tempo 

        
chart = create_chart(x_data_1, [y_data_1, y_data_2], labels, title='Gráfico Infectados Brasil x India')
chart_content = get_api_chart(chart)
salve_image('grafico_brazil_x_india.png', chart_content)
display_image('grafico_brazil_x_india.png')