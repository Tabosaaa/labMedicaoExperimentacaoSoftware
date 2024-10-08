import os
import requests

# URL da API GraphQL do GitHub
GITHUB_API_URL = 'https://api.github.com/graphql'

def exec_search(query, token):
    """Executa uma consulta GraphQL na API do GitHub."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
        response.raise_for_status()  # Lança um erro para códigos de status 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Query falhou: {str(e)}")

def build_query(batch_size, cursor=None):
    """Constrói a string de consulta GraphQL para buscar repositórios em Java."""
    after_cursor = f', after: "{cursor}"' if cursor else ""
    
    query = f"""
    {{
        search(query: "language:Java stars:>1", type: REPOSITORY, first: {batch_size}{after_cursor}) {{
            nodes {{
                ... on Repository {{
                    name
                    owner {{
                        login
                    }}
                    url
                    createdAt
                    updatedAt
                    primaryLanguage {{
                        name
                    }}
                    stargazers {{
                        totalCount
                    }}
                    releases {{
                        totalCount
                    }}
                }}
            }}
            pageInfo {{
                endCursor
                hasNextPage
            }}
        }}
    }}
    """
    return query

def get_all_repositories(repository_number, token, batch_size=20):
    """Retorna uma lista dos repositórios Java mais populares."""
    all_repositories = []
    cursor = None

    while len(all_repositories) < repository_number:
        query = build_query(batch_size, cursor)
        result = exec_search(query, token)

        if 'errors' in result:
            raise Exception(f"Erro na consulta GraphQL: {result['errors']}")

        all_repositories.extend(result['data']['search']['nodes'])

        page_info = result['data']['search']['pageInfo']
        cursor = page_info['endCursor']

        if not page_info['hasNextPage']:
            break  

    return all_repositories[:repository_number] 