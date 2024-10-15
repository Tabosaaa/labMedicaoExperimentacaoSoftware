from dotenv import load_dotenv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("Token de acesso do GitHub não encontrado!")
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

def get_top_starred_repos():
    repos = []
    page = 1
    per_page = 100  
    while len(repos) < 200:
        url = f"https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao buscar repositórios: {response.status_code}")
            break

        data = response.json()
        if "items" in data:
            repos.extend(data['items'])
            page += 1
        else:
            break

    return repos[:200]  

def has_enough_prs(repo_full_name):
    total_prs = 0
    page = 1
    per_page = 100  
    while total_prs < 100:  
        url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=closed&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao buscar PRs para {repo_full_name}: {response.status_code}")
            return False

        prs = response.json()
        total_prs += len(prs)
        
        if len(prs) < per_page:
            break
        page += 1

    return total_prs >= 100

def find_repos_with_prs():
    top_repos = get_top_starred_repos()
    repos_with_prs = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_repo = {executor.submit(has_enough_prs, repo['full_name']): repo for repo in top_repos}
        for future in as_completed(future_to_repo):
            repo = future_to_repo[future]
            try:
                if future.result():  
                    repos_with_prs.append(repo)
            except Exception as exc:
                print(f"Erro ao processar {repo['full_name']}: {exc}")
            
            if len(repos_with_prs) >= 200:
                break

    return repos_with_prs

if __name__ == "__main__":
    repos = find_repos_with_prs()
    print(f"Encontrados {len(repos)} repositórios com mais de 100 PRs.")
    for repo in repos:
        print(f"{repo['full_name']} - Estrelas: {repo['stargazers_count']}")
