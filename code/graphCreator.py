import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Garantindo que a pasta graphs exista
os.makedirs('graphs', exist_ok=True)

# Carregando os arquivos CSV
df1 = pd.read_csv('csv/general_analysis_1000.csv')
df2 = pd.read_csv('csv/language_analysis_1000.csv')
df3 = pd.read_csv('csv/repositories_data_1000.csv')

# RQ 01: Histograma da Idade dos Repositórios
plt.figure(figsize=(10, 6))
sns.histplot(df3['repository_age'], kde=False, bins=10)
plt.title('Distribuição da Idade dos Repositórios Populares')
plt.xlabel('Idade (anos)')
plt.ylabel('Número de Repositórios')
plt.savefig('graphs/histograma_idade_repositorios.png')
plt.close()

# RQ 02: Boxplot do Total de Pull Requests Aceitas
plt.figure(figsize=(10, 6))
sns.boxplot(y=df3['merged_pr_count'])
plt.title('Distribuição de Pull Requests Aceitas')
plt.ylabel('Número de Pull Requests Aceitas')
plt.savefig('graphs/boxplot_pull_requests_aceitas.png')
plt.close()

# RQ 03: Boxplot do Número de Releases
plt.figure(figsize=(10, 6))
sns.boxplot(y=df3['release_version_count'])
plt.title('Distribuição do Número de Releases')
plt.ylabel('Número de Releases')
plt.savefig('graphs/boxplot_numero_releases.png')
plt.close()

# RQ 04: Histograma dos Dias desde a Última Modificação
plt.figure(figsize=(10, 6))
sns.histplot(df3['days_since_last_modification'], kde=False, bins=10)
plt.title('Dias desde a Última Modificação')
plt.xlabel('Dias')
plt.ylabel('Número de Repositórios')
plt.savefig('graphs/histograma_dias_ultima_modificacao.png')
plt.close()

# RQ 05: Gráfico de Barras da Distribuição das Linguagens Populares
plt.figure(figsize=(10, 6))
sns.countplot(x=df3['main_language'], order=df3['main_language'].value_counts().index)
plt.title('Distribuição das Linguagens Populares nos Repositórios')
plt.xlabel('Linguagem')
plt.ylabel('Número de Repositórios')
plt.xticks(rotation=45)
plt.savefig('graphs/grafico_barras_linguagens_populares.png')
plt.close()

# RQ 06: Boxplot da Razão de Resolução de Issues
plt.figure(figsize=(10, 6))
sns.boxplot(y=df3['issue_resolution_ratio'])
plt.title('Distribuição da Razão de Resolução de Issues')
plt.ylabel('Razão de Resolução de Issues')
plt.savefig('graphs/boxplot_resolucao_issues.png')
plt.close()

# RQ 07: Gráficos de Dispersão para Linguagens Populares e Contribuições, Releases, Atualizações
# Contribuições vs Linguagem
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df3['main_language'], y=df3['merged_pr_count'])
plt.title('Contribuições Externas vs Linguagem')
plt.xlabel('Linguagem')
plt.ylabel('Pull Requests Aceitas')
plt.xticks(rotation=45)
plt.savefig('graphs/scatter_contribuicoes_linguagem.png')
plt.close()

# Releases vs Linguagem
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df3['main_language'], y=df3['release_version_count'])
plt.title('Número de Releases vs Linguagem')
plt.xlabel('Linguagem')
plt.ylabel('Número de Releases')
plt.xticks(rotation=45)
plt.savefig('graphs/scatter_releases_linguagem.png')
plt.close()

# Atualizações vs Linguagem
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df3['main_language'], y=df3['days_since_last_modification'])
plt.title('Dias desde a Última Modificação vs Linguagem')
plt.xlabel('Linguagem')
plt.ylabel('Dias desde a Última Modificação')
plt.xticks(rotation=45)
plt.savefig('graphs/scatter_atualizacoes_linguagem.png')
plt.close()