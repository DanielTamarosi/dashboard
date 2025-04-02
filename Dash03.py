#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Script para a geração do DASH
# importando as bibliotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


# In[ ]:


# Configurar a conexão com o SQL Server
def get_connection():
    server = 'dbdatascience.c2ru64hwgln0.us-east-1.rds.amazonaws.com' 
    database = 'DB_SQL_MBA_HIAE'
    username = 'aluno'
    password = 'uUU78jk98#'
    
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None


# In[ ]:


# Função que executa a consulta de estados
def dados_obito():
    conn = get_connection()
    if conn:
        query = """select year(pass.data_admissao) as Ano, 
                   month(pass.DATA_ADMISSAO ) as mes,
                   case when p.sexo=1 then 'Feminino' else 'Masculino' end as Sexo,
                   case when charindex('Óbito: Sim',observacao) > 0 then 'Sim' else 'Não' end Obito,
                   e.estado,
                   count(*) as Quantidade
                   from TB_PACIENTE as P 
                   join tb_passagem as pass on p.ID_PACIENTE = pass.ID_PACIENTE 
                   join tb_endereco as e on e.ID_PACIENTE = p.ID_PACIENTE 
                   group by  year(pass.data_admissao),month(pass.DATA_ADMISSAO ),case when p.sexo=1 then 'Feminino' else 'Masculino' end,
                   case when charindex('Óbito: Sim',observacao) > 0 then 'Sim' else 'Não' end  ,
                   e.estado 
                """ 
                
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()


# In[ ]:


# Função formata número
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor <1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'


# In[ ]:


st.markdown('''DASHBOARD DE Atendimento :heartbeat:''')

#Add widgets to sidebar
#Not only can you add interactivity to your app with widgets, you can organize them into a sidebar. 
#Elements can be passed to st.sidebar using object notation and with notation.

#The following two snippets are equivalent:

# Carrega os dados da consulta SQL
df_Obito = dados_obito()

# Elemina os valores duplicados para Ano
anos_disponiveis = df_Obito["Ano"].unique()
ano_min = int(anos_disponiveis.min())
ano_max = int(anos_disponiveis.max())

anos_selecionados = st.sidebar.slider("Filtrar por Ano:", ano_min, ano_max, (ano_min, ano_max))

# Filtrar o DataFrame com base nos anos selecionados
df_filtrado = df_Obito[(df_Obito["Ano"] >= anos_selecionados[0]) & (df_Obito["Ano"] <= anos_selecionados[1])]

# Cria o filtro do tipo SLIDER
#anos_selecionados = st.sidebar.slider("Filtrar por Ano:", anos_disponiveis)

# Elinima valores duplicados para o campo sexo e adiciona Todos
sexo_opcoes = ["Todos"] + list(df_Obito["Sexo"].unique())   

sexo_selecionado = st.sidebar.multiselect("Filtrar por Sexo:", sexo_opcoes, default=sexo_opcoes)

estado_opcoes = ["Todos"] + list(df_Obito["estado"].unique()) 
anos_estado = st.sidebar.selectbox("Filtrar por estado:", estado_opcoes)

# Aplicando os filtros

df_filtrado = df_Obito[df_Obito["Ano"].isin(anos_selecionados)]  # Filtra pelos anos selecionados

if "Todos" not in sexo_selecionado:
    df_filtrado = df_filtrado[df_filtrado["Sexo"].isin(sexo_selecionado)]  # Filtra pelo sexo selecionado

if anos_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["estado"] == anos_estado]
    
st.write(df_filtrado)



# In[ ]:





# In[ ]:




