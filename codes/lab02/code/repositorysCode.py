import os
import subprocess

def clone_repositories(repositories):
    """Clona uma lista de repositórios GitHub, ignorando os já clonados."""
    base_dir = "codes/lab02/repositories"  # Pasta onde os repositórios serão clonados
    os.makedirs(base_dir, exist_ok=True)
    
    for repo in repositories:
        repo_url = f"https://github.com/{repo['owner']['login']}/{repo['name']}.git"
        repo_dir = os.path.join(base_dir, repo['name'])
        
        # Verifica se o diretório já foi clonado e se é um repositório Git válido
        if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
            print(f"Repositório {repo['name']} já foi clonado e é um repositório Git válido.")
        else:
            # Clona o repositório se ainda não foi clonado ou não é válido
            subprocess.run(["git", "clone", repo_url, repo_dir])
            print(f"Clonando {repo_url}")




def run_ck_on_repositories(base_dir, output_dir="codes/lab02/csv", use_jars="false", max_files_partition=0, var_field_metrics="false"):
    """Executa CK em todos os repositórios clonados e salva os arquivos CSV em um diretório específico."""
    jar_path = "/Users/tabosa/ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
    
    # Cria o diretório de saída se ele não existir
    os.makedirs(output_dir, exist_ok=True)
    
    for repo_dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, repo_dir)
        if os.path.isdir(full_path):
            print(f"Executando CK no repositório {repo_dir}")
            
            # Define o diretório de saída para este repositório
            repo_output_dir = os.path.join(output_dir, repo_dir)
            os.makedirs(repo_output_dir, exist_ok=True)
            
            # Executa o CK com os parâmetros obrigatórios
            subprocess.run([
                "java", "-jar", jar_path, 
                full_path,                # Diretório do projeto
                use_jars,                 # Uso de JARs (true/false)
                str(max_files_partition),  # Máximo de arquivos por partição
                var_field_metrics,         # Métricas de variáveis e campos (true/false)
                repo_output_dir            # Diretório de saída
            ])
            print(f"Relatórios CK salvos em: {repo_output_dir}")