import pandas as pd
from datetime import datetime

def transform_repository_data(raw_repositories):
    """
    Transforma os dados brutos de repositórios GitHub em um DataFrame organizado.
    
    Parâmetros:
        raw_repositories (list): Lista contendo os dados brutos dos repositórios.
    
    Retorna:
        pd.DataFrame: DataFrame com os dados processados e organizados.
    """
    try:
        repository_dict = {
            "repo_name": [],
            "creation_date": [],
            "main_language": [],
            "stars_count": [],
            "merged_pr_count": [],
            "release_version_count": [],
            "last_modified_date": [],
            "total_issue_count": [],
            "closed_issue_count": [],
            "issue_resolution_ratio": []
        }

        if isinstance(raw_repositories, list):
            for repository in raw_repositories:
                if not isinstance(repository, dict):
                    print(f"Invalid repository data structure skipped: {repository}")
                    continue

                repository_dict["repo_name"].append(repository.get("name", "N/A"))
                repository_dict["creation_date"].append(repository.get("createdAt", "N/A"))
                
                main_language = repository.get("primaryLanguage")
                repository_dict["main_language"].append(main_language.get("name", "Unknown") if main_language else "Unknown")
                
                repository_dict["stars_count"].append(repository.get("stargazers", {}).get("totalCount", 0))
                repository_dict["merged_pr_count"].append(repository.get("pullRequests", {}).get("totalCount", 0))
                repository_dict["release_version_count"].append(repository.get("releases", {}).get("totalCount", 0))
                repository_dict["last_modified_date"].append(repository.get("updatedAt", "N/A"))
                repository_dict["total_issue_count"].append(repository.get("issues", {}).get("totalCount", 0))
                repository_dict["closed_issue_count"].append(repository.get("closedIssues", {}).get("totalCount", 0))
                
                resolution_ratio = (repository_dict["closed_issue_count"][-1] / repository_dict["total_issue_count"][-1]
                                    if repository_dict["total_issue_count"][-1] > 0 else None)
                repository_dict["issue_resolution_ratio"].append(resolution_ratio)

        df = pd.DataFrame(repository_dict)

        # Calcular a idade do repositório em anos
        df['repository_age'] = pd.to_numeric(
            df['creation_date'].apply(lambda x: datetime.now().year - datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year),
            errors='coerce'
        )

        # Calcular o número de dias desde a última modificação
        df['days_since_last_modification'] = pd.to_numeric(
            (pd.to_datetime('now') - pd.to_datetime(df['last_modified_date']).dt.tz_localize(None)).dt.days,
            errors='coerce'
        )

        return df

    except Exception as e:
        raise Exception(f"Failed to process repository data: {e}")


def perform_general_analysis(df):
    """
    Realiza uma análise geral dos dados dos repositórios.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados dos repositórios.
    
    Retorna:
        dict: Dicionário contendo as métricas medianas calculadas.
    """
    try:
        general_metrics = {
            "median_repository_age": df['repository_age'].median(),
            "median_merged_pull_requests": df['merged_pr_count'].median(),
            "median_releases": df['release_version_count'].median(),
            "median_update_interval_days": df['days_since_last_modification'].median(),
            "median_issue_resolution_ratio": df['issue_resolution_ratio'].median()
        }
        return general_metrics

    except Exception as e:
        raise Exception(f"Error during general analysis: {e}")
        

def perform_language_analysis(df):
    """
    Realiza uma análise por linguagem dos dados dos repositórios.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados dos repositórios.
    
    Retorna:
        dict: Dicionário contendo a contagem de repositórios por linguagem popular e demais linguagens.
    """
    try:
        # Principais linguagens populares
        popular_languages = [
            'JavaScript', 'Python', 'TypeScript', 'Java', 'C#',
            'C++', 'PHP', 'C', 'Shell', 'Go'
        ]

        # Contagem de repositórios por linguagem
        language_distribution = df['main_language'].value_counts()

        # Filtrar para considerar apenas as linguagens mais populares
        popular_language_distribution = language_distribution[language_distribution.index.isin(popular_languages)]

        # Prepara o resultado para retorno
        language_metrics = {
            "total_repositories_analyzed": len(df),
            "distribution_of_popular_languages": popular_language_distribution.to_dict(),
            "count_of_other_languages": language_distribution[~language_distribution.index.isin(popular_languages)].sum()
        }

        return language_metrics

    except Exception as e:
        raise Exception(f"Error during language analysis: {e}")



def export_dataframe_to_csv(df, filename):
    """
    Exporta o DataFrame para um arquivo CSV.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame a ser exportado.
        filename (str): Nome do arquivo CSV.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to: {filename}")
    except Exception as e:
        raise Exception(f"Error saving data to CSV: {e}")
