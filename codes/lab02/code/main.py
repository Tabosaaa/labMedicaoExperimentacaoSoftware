import os
from dotenv import load_dotenv
from execSearch import get_all_repositories
from repositorysCode import clone_repositories,run_ck_on_repositories

load_dotenv()

token = os.getenv("TOKEN")

if not token:
    raise Exception("Você precisa configurar a variável \"TOKEN\" no arquivo .env") 

number_of_repositories = 5

data = get_all_repositories(number_of_repositories, token=token)

clone_repositories(data)
run_ck_on_repositories(base_dir="codes/lab02/repositories")

