import os
import subprocess
import shutil

class Repository:
    """Representa um repositório GitHub e suas operações."""

    def __init__(self, owner, name, base_dir="codes/lab02/repositories"):
        self.owner = owner
        self.name = name
        self.url = f"https://github.com/{self.owner}/{self.name}.git"
        self.base_dir = base_dir
        self.local_path = os.path.join(self.base_dir, self.name)

    def clone(self):
        """Clona o repositório no diretório local."""
        os.makedirs(self.base_dir, exist_ok=True)
        print(f"Clonando {self.url}")
        subprocess.run(["git", "clone", self.url, self.local_path])

    def delete(self):
        """Exclui o repositório clonado do diretório local."""
        if os.path.exists(self.local_path):
            shutil.rmtree(self.local_path)
            print(f"Repositório {self.name} excluído.")
        else:
            print(f"O diretório {self.local_path} não existe.")