from typing import final
import requests as r
import csv
import datetime as dt
from PIL import Image
from  IPython.display import display
from requests.api import options

#Recebendo os dados do site
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=BRL&apikey='# key = Colocar a sua Key
resp = r.get(url)
data = resp.json() # Transformando esses Dados em um arquivo .json

dados = []  #Filtrando os dados, iremos guardar nessa lista apenas os dados desejados

for x in data['Time Series (Digital Currency Monthly)']:
    dados.append([data['Time Series (Digital Currency Monthly)'][x]['4a. close (BRL)'], x]) # Colocando a data e o valor do Bitcoin na lista

dados.insert(0, ['Preco','Data']) # Criando o Headline da lista

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
        'display' : display,
        "width": 1920,
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
            'options': options,
            
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

dados = dados[::-1]


# Atribuindo os dados de Brasil e india aos valores do gráfico
y_data_1 = []

for obs in dados[9:]:
    y_data_1.append(obs[0]) # Adicionando ao eixo Y do gráfico os infecatdos do Brasil


labels = ['Valor Bitcoin em BRL (Real)'] # Colunas do gráfico

x_data_1 = []
for obs in dados[9:]:
    x_data_1.append(obs[1]) # Adciando ao eixo X do gráfico o tempo 

#Chamando as funções para gerar e salvar o arquivo   
chart = create_chart(x_data_1, y_data_1, labels, title='Crescimento_valor_Bitcoin')
chart_content = get_api_chart(chart)
salve_image('Crescimento_valor_Bitcoin.png', chart_content)



