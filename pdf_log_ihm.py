import json
import pdfkit
from io import BytesIO
from bs4 import BeautifulSoup
from datetime import datetime


now = datetime.now()
dt_string = now.strftime("%Y-%m-%d")

grouped_data = {}

# Ler o arquivo JSON
with open('700002.json', 'r', encoding='utf-8') as file:
    obj = json.load(file)

# Agrupar os dados por nome da máquina e operador
for item in obj:
    machine_id = str(item['machine']['description'])
    operator_name = item["operator"]["name"] if item["operator"] else "null"
    date_str = item['timestamp'].replace('Z', '')
    date = datetime.fromisoformat(date_str).strftime('%Y-%m-%d')
    if date not in grouped_data:
        grouped_data[date] = {}
    if machine_id not in grouped_data[date]:
        grouped_data[date][machine_id] = []
    grouped_data[date][machine_id].append(item)
# Exibir os dados agrupados
# print(json.dumps(grouped_data, indent=2))

# Upload data to S3

def generate_pdf(data, file_name):
    options = {
        'enable-local-file-access': None,
        'encoding': 'utf-8',
    }

    # Ler o conteúdo do arquivo HTML
    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()

    # Criar objeto Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')

    # Manipular o HTML conforme necessário (exemplo: alterar o título da página)
    soup.h5.string = 'Data: '+dt_string
    
    # Encontre o elemento 'label' com a classe 'machine'
    label_machine = soup.find('label', class_='machine')

    # Adicione novo conteúdo à tag 'label'
    if label_machine:
        label_machine.append(''+machine_id)
    
    # Encontre o elemento 'label' com a classe 'operator'
    label_operator = soup.find('label', class_='operator')

    # Adicione novo conteúdo à tag 'label'
    if label_operator:
        label_operator.append(''+operator_name)

    # Encontre a tabela com a classe 'example-class'
    table = soup.find('table', class_='table')
    # Adicionar uma nova linha à tabela
    if table:
        for log in data:
            # print(log)
            new_row = soup.new_tag('tr')
            
            new_name = soup.new_tag('td')
            new_name.string = log
            new_row.append(new_name)
            
            new_age = soup.new_tag('td')
            new_age.string = '32'
            new_row.append(new_age)
            
            new_age = soup.new_tag('td')
            new_age.string = '32'
            new_row.append(new_age)
            
            new_age = soup.new_tag('td')
            new_age.string = '32'
            new_row.append(new_age)
            
            table.append(new_row)


    # Converter o objeto Beautiful Soup de volta para uma string HTML
    html_modificado = str(soup)
   
    # Gerar PDF a partir da string HTML
    pdfkit.from_string(html_modificado, file_name, options=options)


# client = boto3.client('s3')
for date, machines in grouped_data.items():
    for machine_id, items in machines.items():
        data_string = json.dumps(items, indent=2, default=str)
        file_name = f'{date}_{machine_id}.pdf'
        # print(data_string)
        generate_pdf(data_string, file_name)



