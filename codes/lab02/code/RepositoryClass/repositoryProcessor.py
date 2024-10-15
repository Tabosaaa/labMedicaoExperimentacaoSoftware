import os
from datetime import datetime
import pandas as pd
from RepositoryClass.repository import Repository
from CKrunner.CKrunner import CKRunner
from execSearch import get_all_repositories

class RepositoryProcessor:
    """Processa uma lista de repositórios: clona, executa CK e exclui."""

    def __init__(self, token, number_of_repositories, jar_path):
        self.token = token
        self.number_of_repositories = number_of_repositories
        self.jar_path = jar_path
        self.repositories_data = get_all_repositories(self.number_of_repositories, token=self.token)
        self.ck_runner = CKRunner(jar_path=self.jar_path,)
        self.repos_metrics = []  # Lista para armazenar as métricas de cada repositório

    def process_all(self):
        """Processa todos os repositórios obtidos."""
        aux = 1
        for repo_data in self.repositories_data:
            owner = repo_data['owner']['login']
            name = repo_data['name']
            repository = Repository(owner=owner, name=name)
            repository.clone()

            # Executa o CK no repositório
            self.ck_runner.run(repository)

            # Exclui o repositório clonado
            repository.delete()

            # Coleta as métricas adicionais do repositório
            stars = repo_data['stargazers']['totalCount']
            releases = repo_data['releases']['totalCount']
            created_at = repo_data['createdAt']

            # Calcula a maturidade (idade em anos)
            created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            now = datetime.utcnow()
            maturity_years = (now - created_date).days / 365.25  # Aproximação de anos

            # Armazena as métricas em um dicionário
            repo_metrics = {
                'repository': name,
                'owner': owner,
                'stars': stars,
                'releases': releases,
                'maturity_years': round(maturity_years, 2)
            }

            self.repos_metrics.append(repo_metrics)

            print(f"Repositório número {aux}")
            aux += 1

        # Após processar todos os repositórios, salva as métricas em um CSV
        self.save_repos_metrics()

    def save_repos_metrics(self):
        """Salva as métricas dos repositórios em um arquivo CSV."""
        output_dir = 'codes/lab02/csv'
        os.makedirs(output_dir, exist_ok=True)
        metrics_csv_path = os.path.join(output_dir, "repos_metrics.csv")

        # Cria um DataFrame a partir das métricas coletadas
        metrics_df = pd.DataFrame(self.repos_metrics)

        # Salva o DataFrame em um arquivo CSV
        metrics_df.to_csv(metrics_csv_path, index=False)
        print(f"Métricas dos repositórios salvas em {metrics_csv_path}")