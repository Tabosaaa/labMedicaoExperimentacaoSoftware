import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Leitura dos dados
df = pd.read_csv('results.csv')

# Criação do gráfico
fig = go.Figure()

# Adiciona os pontos de dispersão
fig.add_trace(go.Scatter(
    x=df['any'],
    y=df['specific_types'],
    mode='markers',
    marker=dict(color='purple', opacity=0.6),
    name='Dados'
))

# Adiciona a linha y = x
fig.add_trace(go.Scatter(
    x=[0, 5000],
    y=[0, 5000],
    mode='lines',
    line=dict(color='red', dash='dash'),
    name='y = x'
))

# Configurações do layout
fig.update_layout(
    title='Comparação entre Quantidade de "any" e "specific_types" por Projeto',
    xaxis_title='Quantidade de "any"',
    yaxis_title='Quantidade de "specific_types"',
    xaxis=dict(range=[0, 5000]),
    yaxis=dict(range=[0, 5000]),
    legend=dict(title='Legenda'),
    plot_bgcolor='white'
)

# Adiciona linhas de grade
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Exibe o gráfico no Streamlit
st.plotly_chart(fig)

total_ts_loc = df['TLOC'].sum()
total_js_loc = df['JS_LOC'].sum()

mean_ts_loc = df['TLOC'].mean()
mean_js_loc = df['JS_LOC'].mean()

# Título principal
st.title("Comparação de Linhas de Código entre TypeScript e JavaScript")

# Dados para os gráficos
data_totais = pd.DataFrame({
    'Linguagem': ['TypeScript', 'JavaScript'],
    'Total de Linhas de Código': [total_ts_loc, total_js_loc]
})

data_medias = pd.DataFrame({
    'Linguagem': ['TypeScript', 'JavaScript'],
    'Média de Linhas de Código por Projeto': [mean_ts_loc, mean_js_loc]
})

# Gráfico de barras para os totais
fig_totais = px.bar(
    data_totais,
    x='Linguagem',
    y='Total de Linhas de Código',
    color='Linguagem',
    title='Total de Linhas de Código por Linguagem',
    text='Total de Linhas de Código'
)
fig_totais.update_layout(showlegend=False)
fig_totais.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# Exibição do gráfico de totais
st.plotly_chart(fig_totais)

# Gráfico de barras para as médias
fig_medias = px.bar(
    data_medias,
    x='Linguagem',
    y='Média de Linhas de Código por Projeto',
    color='Linguagem',
    title='Média de Linhas de Código por Projeto por Linguagem',
    text='Média de Linhas de Código por Projeto'
)
fig_medias.update_layout(showlegend=False)
fig_medias.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# Exibição do gráfico de médias
st.plotly_chart(fig_medias)

strict_lost = df[(df['prev_year_strict'] == True) & (df['strict'] == False)]
strict_lost_count = len(strict_lost)

# Total de repositórios que tinham 'strict' ativado no ano anterior
prev_year_strict_count = df['prev_year_strict'].sum()

# Dados para o gráfico
labels = ['Perderam Strict', 'Mantiveram Strict']
values = [strict_lost_count, prev_year_strict_count - strict_lost_count]

data = pd.DataFrame({
    'Status': labels,
    'Quantidade': values
})

# Criação do gráfico de pizza com Plotly
fig = px.pie(
    data,
    names='Status',
    values='Quantidade',
    title='Comparação de Repositórios: Strict Ativado no Ano Anterior, mas Desativado Agora',
    color='Status',
    color_discrete_map={'Perderam Strict':'red', 'Mantiveram Strict':'green'},
    hole=0
)

# Atualização das informações do texto no gráfico
fig.update_traces(textinfo='percent+label')

# Exibição do gráfico no Streamlit
st.plotly_chart(fig)



# Criação do gráfico de dispersão
fig = go.Figure()

# Adiciona os pontos de dispersão
fig.add_trace(go.Scatter(
    x=df['qty_ts_files'],
    y=df['qty_js_files'],
    mode='markers',
    marker=dict(color='purple', opacity=0.6),
    name='Projetos'
))

# Adiciona a linha y = x
fig.add_trace(go.Scatter(
    x=[0, 10000],
    y=[0, 10000],
    mode='lines',
    line=dict(color='red', dash='dash'),
    name='y = x'
))

# Configurações do layout
fig.update_layout(
    title='Relação entre Arquivos JS e TS por Projeto',
    xaxis_title='Quantidade de Arquivos TS (TypeScript)',
    yaxis_title='Quantidade de Arquivos JS (JavaScript)',
    xaxis=dict(range=[0, 10000]),
    yaxis=dict(range=[0, 10000]),
    legend=dict(title='Legenda'),
    plot_bgcolor='white',
    width=800,
    height=600
)

# Adiciona linhas de grade
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Exibe o gráfico no Streamlit
st.plotly_chart(fig)

def any_plot(df_filtered):
    # Determina o valor máximo para ajustar a linha y = x
    max_value = max(df_filtered['any'].max(), df_filtered['prev_year_any'].max())

    # Criação do gráfico de dispersão
    fig = go.Figure()

    # Adiciona os pontos de dispersão
    fig.add_trace(go.Scatter(
        x=df_filtered['prev_year_any'],
        y=df_filtered['any'],
        mode='markers',
        marker=dict(color='purple', opacity=0.6),
        name='Projetos'
    ))

    # Adiciona a linha y = x
    fig.add_trace(go.Scatter(
        x=[0, max_value],
        y=[0, max_value],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='y = x'
    ))

    # Configurações do layout
    fig.update_layout(
        title='Comparação da Quantidade de Any por Projeto (Ano Anterior vs Atual)',
        xaxis_title='Quantidade de Any (Ano Anterior)',
        yaxis_title='Quantidade de Any (Atual)',
        legend=dict(title='Legenda'),
        plot_bgcolor='white',
        width=800,
        height=600
    )

    # Adiciona linhas de grade
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def boxplot_any(df_filtered):
    # Criação do boxplot
    fig = go.Figure()

    fig.add_trace(go.Box(
        x=df_filtered['prev_year_any'],
        name='Ano Anterior',
        orientation='h',
        boxmean=True
    ))
    fig.add_trace(go.Box(
        x=df_filtered['any'],
        name='Atual',
        orientation='h',
        boxmean=True
    ))

    # Configurações do layout
    fig.update_layout(
        title='Boxplot da Quantidade de Any (Ano Anterior vs Atual)',
        xaxis_title='Quantidade de Any',
        yaxis_title='',
        plot_bgcolor='white',
        width=800,
        height=600,
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Ano Anterior', 'Atual']
        )
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

df_filtered = df[df['prev_year_any'] <= 900]

# Título da aplicação
st.title('Análise da Quantidade de Any por Projeto')

# Geração e exibição dos gráficos
any_plot(df_filtered)
boxplot_any(df_filtered)


def ts_ignore_plot(df):
    # Determina o valor máximo para ajustar a linha y = x
    max_value_x = df['prev_year_ts_ignore'].max()
    max_value_y = df['ts_ignore'].max()
    max_value = max(max_value_x, max_value_y)

    # Criação do gráfico de dispersão
    fig = go.Figure()

    # Adiciona os pontos de dispersão
    fig.add_trace(go.Scatter(
        x=df['prev_year_ts_ignore'],
        y=df['ts_ignore'],
        mode='markers',
        marker=dict(color='purple', opacity=0.6),
        name='Projetos'
    ))

    # Adiciona a linha y = x
    fig.add_trace(go.Scatter(
        x=[0, max_value],
        y=[0, max_value],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='y = x'
    ))

    # Configurações do layout
    fig.update_layout(
        title='Comparação da Quantidade de TS Ignore por Projeto (Ano Anterior vs Atual)',
        xaxis_title='Quantidade de TS Ignore (Ano Anterior)',
        yaxis_title='Quantidade de TS Ignore (Atual)',
        xaxis=dict(range=[0, 80]),
        yaxis=dict(range=[0, 100]),
        legend=dict(title='Legenda'),
        plot_bgcolor='white',
        width=800,
        height=600
    )

    # Adiciona linhas de grade
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def boxplot_ts_ignore(df):
    # Criação do boxplot
    fig = go.Figure()

    # Adiciona os boxplots
    fig.add_trace(go.Box(
        y=df['prev_year_ts_ignore'],
        name='Ano Anterior',
        boxmean=True,
        marker_color='blue'
    ))

    fig.add_trace(go.Box(
        y=df['ts_ignore'],
        name='Atual',
        boxmean=True,
        marker_color='green'
    ))

    # Configurações do layout
    fig.update_layout(
        title='Boxplot da Quantidade de TS Ignore (Ano Anterior vs Atual)',
        yaxis_title='Quantidade de TS Ignore',
        xaxis_title='',
        plot_bgcolor='white',
        width=600,
        height=600
    )

    # Aplica escala logarítmica no eixo Y, se necessário
    fig.update_yaxes(type='log', dtick=1)

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)
    
    # Título da aplicação
st.title('Análise da Quantidade de TS Ignore por Projeto')

    # Geração e exibição dos gráficos
ts_ignore_plot(df)
boxplot_ts_ignore(df)