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
        """Executa o CK no repositório fornecido e retorna loc e linhas de comentários."""
        temp_output_dir = os.path.join(self.output_base_dir, "temp")
        os.makedirs(temp_output_dir, exist_ok=True)

        print(f"Executando CK no repositório em {repository.local_path}")
        subprocess.run([
            "java", "-jar", self.jar_path,
            repository.local_path,
            self.use_jars,
            str(self.max_files_partition),
            self.var_field_metrics,
            temp_output_dir
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        # Remove o diretório temporário
        shutil.rmtree(temp_output_dir)
        print(f"Dados do CK processados para {repository.name}.")
