import os
import subprocess
import shutil
import pandas as pd

class CKRunner:
    """Executa o CK em um repositório e extrai as métricas necessárias."""

    def __init__(self, jar_path, output_base_dir="codes/lab02/csv", use_jars="false", max_files_partition=0, var_field_metrics="false"):
        self.jar_path = jar_path
        self.output_base_dir = output_base_dir
        self.use_jars = use_jars
        self.max_files_partition = max_files_partition
        self.var_field_metrics = var_field_metrics

    def run(self, repository):
        repo_output_dir = os.path.join(self.output_base_dir, repository.name)

        print(f"Executando CK no repositório em {repository.local_path}")
        subprocess.run([
            "java", "-jar", self.jar_path,
            repository.local_path,
            self.use_jars,
            str(self.max_files_partition),
            self.var_field_metrics,
            repo_output_dir
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        print(f"Dados do CK processados para {repository.name}.")
