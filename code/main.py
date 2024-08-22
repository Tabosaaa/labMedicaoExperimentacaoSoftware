import os
import pandas as pd
from dotenv import load_dotenv
from execSearch import get_all_repositories
from processData import transform_repository_data, export_dataframe_to_csv, perform_general_analysis, perform_language_analysis

load_dotenv()

token = os.getenv("TOKEN")

if not token:
    raise Exception("Você precisa configurar a variável \"TOKEN\" no arquivo .env") 

number_of_repositories = 100

data = get_all_repositories(number_of_repositories, token=token)

transformed_data = transform_repository_data(data)

export_dataframe_to_csv(transformed_data, filename=f'repositories_data_{number_of_repositories}.csv')


general_analysis = perform_general_analysis(transformed_data)
language_analysis = perform_language_analysis(transformed_data)


general_df = pd.DataFrame([general_analysis])
language_df = pd.DataFrame.from_dict(language_analysis).reset_index()

general_df.to_csv(f'general_analysis_{number_of_repositories}.csv', index=False)
language_df.to_csv(f'language_analysis_{number_of_repositories}.csv', index=False)

print("Análise feita com sucesso")