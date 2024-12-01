import requests
import time
import csv
import random

# Configurações
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
URL = 'https://api.github.com/search/repositories'

# Número de requisições
NUM_REQUESTS = 1000

# Intervalo entre requisições (em segundos)
REQUEST_INTERVAL = 2

# Lista de linguagens de programação para variar as consultas
LANGUAGES = ['Python', 'JavaScript', 'Java', 'Go', 'Ruby', 'C++', 'Swift', 'Kotlin']

def rest():
    results = []

    for i in range(NUM_REQUESTS):
        # Escolher aleatoriamente uma linguagem de programação
        language = random.choice(LANGUAGES)

        # Escolher aleatoriamente o número de resultados por página
        per_page = random.randint(1, 100)  # Entre 1 e 100

        # Parâmetros da busca
        params = {
            'q': f'language:{language}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page
        }

        start_time = time.time()
        response = requests.get(URL, headers=HEADERS, params=params)
        end_time = time.time()

        response_time = end_time - start_time
        response_size = len(response.content)

        results.append({
            'request_number': i + 1,
            'response_time': response_time,
            'response_size': response_size,
            'language': language,
            'per_page': per_page
        })

        # Imprimir progresso a cada 10 requisições
        if (i + 1) % 10 == 0:
            print(f'Requisição REST {i + 1}/{NUM_REQUESTS} concluída.')

        # Aguardar intervalo para respeitar o limite de taxa
        time.sleep(REQUEST_INTERVAL)

    # Salvar resultados em um arquivo CSV
    with open('rest_api_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['request_number', 'response_time', 'response_size', 'language', 'per_page']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print('Teste da API REST concluído. Resultados salvos em rest_api_results.csv.')

