import os
from dotenv import load_dotenv
from RepositoryClass.repositoryProcessor import RepositoryProcessor

load_dotenv()

token = os.getenv("TOKEN")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        raise Exception("Você precisa configurar a variável \"TOKEN\" no arquivo .env")

    number_of_repositories = 4
    jar_path = "/Users/tabosa/ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

    processor = RepositoryProcessor(token, number_of_repositories, jar_path)
    processor.process_all()