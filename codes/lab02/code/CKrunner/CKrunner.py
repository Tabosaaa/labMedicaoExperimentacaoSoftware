import os
import subprocess
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
        
        method_file = repository.name+"method.csv"
        class_file = repository.name+"class.csv"
        
        repo_method_csv = self.output_base_dir+"/"+method_file
        repo_class_csv = self.output_base_dir+"/"+class_file

        # Append the data from the method and class files to the repository files
        self.append_files(repo_method_csv, "codes/lab02/csv/methods.csv")
        self.append_files(repo_class_csv, "codes/lab02/csv/classes.csv")


        os.remove(repo_method_csv)
        os.remove(repo_class_csv)

        print(f"Dados do CK processados para {repository.name}.")

    def append_files(self, x, y):
        """Appends the data from file x to file y.

        Args:
            x (str): Path to the source file (to read from).
            y (str): Path to the target file (to append to).
        """

        # Check if the source file exists
        if not os.path.exists(x):
            raise FileNotFoundError(f"Arquivo de origem '{x}' não existe.")

        # Read data from the source file
        try:
            source_df = pd.read_csv(x)
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo de origem '{x}': {e}")

        # Check if the target file exists
        if os.path.exists(y):
            # Read data from the target file
            try:
                target_df = pd.read_csv(y)
            except Exception as e:
                raise IOError(f"Erro ao ler o arquivo de destino '{y}': {e}")

            # Verify that the columns match
            if list(source_df.columns) != list(target_df.columns):
                raise ValueError("As colunas dos arquivos não correspondem.")

            # Append the source data to the target data
            combined_df = pd.concat([target_df, source_df], ignore_index=True)
        else:
            # If the target file doesn't exist, use the source data as the combined data
            combined_df = source_df

        # Write the combined data back to the target file
        try:
            combined_df.to_csv(y, index=False)
        except Exception as e:
            raise IOError(f"Erro ao escrever no arquivo de destino '{y}': {e}")
            
