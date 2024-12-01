import requests
import time
import csv
import os 
import random
from dotenv import load_dotenv

load_dotenv()

# Configurações
GITHUB_TOKEN =  os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'bearer {GITHUB_TOKEN}'}
URL = 'https://api.github.com/graphql'

# Número de requisições
NUM_REQUESTS = 1000
REQUEST_INTERVAL = 2

# Lista de linguagens de programação para variar as consultas
LANGUAGES = ['Python', 'JavaScript', 'Java', 'Go', 'Ruby', 'C++', 'Swift', 'Kotlin']

def graphql():
    results = []

    for i in range(NUM_REQUESTS):
        # Escolher aleatoriamente uma linguagem de programação
        language = random.choice(LANGUAGES)

        # Escolher aleatoriamente o número de resultados
        first = random.randint(1, 50)  # Entre 1 e 50

        # Query GraphQL com parâmetros variáveis
        query = f"""
        {{
          search(query: "language:{language}", type: REPOSITORY, first: {first}) {{
            edges {{
              node {{
                ... on Repository {{
                  name
                  owner {{
                    login
                  }}
                  stargazerCount
                  description
                  languages(first: 5) {{
                    nodes {{
                      name
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        start_time = time.time()
        response = requests.post(URL, json={'query': query}, headers=HEADERS)
        end_time = time.time()

        response_time = end_time - start_time
        response_size = len(response.content)

        results.append({
            'request_number': i + 1,
            'response_time': response_time,
            'response_size': response_size,
            'language': language,
            'first': first
        })

        # Imprimir progresso a cada 10 requisições
        if (i + 1) % 10 == 0:
            print(f'Requisição GraphQL {i + 1}/{NUM_REQUESTS} concluída.')

        # Aguardar intervalo para respeitar o limite de taxa
        time.sleep(REQUEST_INTERVAL)

    # Salvar resultados em um arquivo CSV
    with open('graphql_api_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['request_number', 'response_time', 'response_size', 'language', 'first']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print('Teste da API GraphQL concluído. Resultados salvos em graphql_api_results.csv.')

