import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go




st.set_page_config(layout="wide")
# leitura do banco de dados
df = pd.read_csv('base_de_dados_previa.csv',encoding='cp1252',sep=';')
df['meq'] = df['meq'].str.replace(',','.').astype(float)
df['meqrap'] = df['meqrap'].str.replace(',','.').astype(float)
#ajustes no df
df['Campus'] = df['Campus'].str.upper()
df['DS_EIXO_TECNOLOGICO'] = df['DS_EIXO_TECNOLOGICO'].fillna('-')
df_eficiencia = pd.read_csv('eficiencia.csv',sep=';',encoding='cp1252')
df_eficiencia = df_eficiencia.fillna(0.0)
df_docentes = pd.read_csv('docentes.csv', encoding='cp1252',sep=';')
df_docentes['contagem'] = df_docentes['contagem'].str.replace(',','.').astype(float)
df_docentes.info()
df_docentes_por_campus = df_docentes.groupby('Campus')['contagem'].sum().reset_index()
df_docentes_por_campus = df_docentes_por_campus.rename(columns={'Campus':'Campus','contagem':'docentes'})
df_docentes_por_campus['Campus'] = df_docentes_por_campus['Campus'].str.upper()

# construção da barra lateral
col1,col2, col3=st.columns([1,4,9])
col1.image('ifpa_logo.png'  )
col3.markdown("""
    #       PNP Prévia IFPA 2024
    """)
painel = ['Matrículas por campus','Matrículas por tipo, eixo e curso','Matrículas equivalentes por campus','Matrículas equivalentes por tipo, eixo e curso', 'RAP', 'Eficiência Acadêmica']
painel_escolhido = st.selectbox('Selecione o Painel desejado:', painel)

def matriculas_por_campus():
    st.markdown('# '+ painel_escolhido)

    tipos_de_curso = ['TODOS'] + sorted(df['DS_TIPO_CURSO'].unique())
    eixos_tecnologicos = ['TODOS'] + sorted(df['DS_EIXO_TECNOLOGICO'].unique())
    nomes_de_curso = ['TODOS'] + sorted(df['NO_CURSO'].unique())
    tipo = st.selectbox('Selecione o tipo de curso:', tipos_de_curso)
    if tipo == 'TODOS':
        df_tipo = df
    else:
        df_tipo = df[df['DS_TIPO_CURSO'] == tipo]
        eixos_tecnologicos = ['TODOS'] + sorted(df_tipo['DS_EIXO_TECNOLOGICO'].unique())
    eixo = st.selectbox('Selecione o eixo tecnológico:', eixos_tecnologicos)
    if eixo == 'TODOS':
        df_eixo = df_tipo
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    else:
        df_eixo = df_tipo[df_tipo['DS_EIXO_TECNOLOGICO'] == eixo]
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    curso = st.selectbox('Selecione o curso:', nomes_de_curso)

    if tipo == 'TODOS':
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_figura = df.groupby('Campus')['Nome'].count().reset_index()
            else:
                df_campus = df[df['NO_CURSO'] == curso]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
        else:
            if curso == 'TODOS':
                df_campus = df[df['DS_EIXO_TECNOLOGICO'] == eixo]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
            else:
                df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
    else:
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_campus = df[df['DS_TIPO_CURSO'] == tipo]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
            else:
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
        else:
            if curso == 'TODOS':
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()
            else:
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['Nome'].count().reset_index()


    col1,col2,col3 = st.columns([1,1,9])
    total = df_figura['Nome'].sum()
    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(value=total, number={"valueformat": ".0f"},title={'text':'TOTAL', 'font':{'family':'Times New Roman','size':48}}))
    col1.plotly_chart(fig2)
    fig1 = px.treemap(df_figura, path=[px.Constant('IFPA'), 'Campus'], values='Nome', color='Campus', height=800)
    fig1.data[0].textinfo = 'label+text+value'
    fig1.layout.hovermode = False
    col3.plotly_chart(fig1)
    
def matriculas_por_tipo_eixo_curso():
    st.markdown('# '+ painel_escolhido)

    lista_de_campus = ['TODOS'] + sorted(df['Campus'].unique())
    tipos_de_curso = ['TODOS'] + sorted(df['DS_TIPO_CURSO'].unique())
    eixos_tecnologicos = ['TODOS'] + sorted(df['DS_EIXO_TECNOLOGICO'].unique())
    nomes_de_curso = ['TODOS'] + sorted(df['NO_CURSO'].unique())
    campus = st.selectbox('Selecione o campus:', lista_de_campus)
    if campus == 'TODOS':
        df_campus = df
    else:
        df_campus = df[df['Campus'] == campus]
    tipo = st.selectbox('Selecione o tipo de curso:', tipos_de_curso)
    if tipo == 'TODOS':
        df_tipo = df_campus
    else:
        df_tipo = df_campus[df_campus['DS_TIPO_CURSO'] == tipo]
        eixos_tecnologicos = ['TODOS'] + sorted(df_tipo['DS_EIXO_TECNOLOGICO'].unique())
    eixo = st.selectbox('Selecione o eixo tecnológico:', eixos_tecnologicos)
    if eixo == 'TODOS':
        df_eixo = df_tipo
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    else:
        df_eixo = df_tipo[df_tipo['DS_EIXO_TECNOLOGICO'] == eixo]
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    curso = st.selectbox('Selecione o curso:', nomes_de_curso)

    if campus == 'TODOS':
        if tipo == 'TODOS':
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus=df
                else:
                    df_campus = df[df['NO_CURSO'] == curso]
            else:
                if curso == 'TODOS':
                    df_campus = df[df['DS_EIXO_TECNOLOGICO'] == eixo]
                else:
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
        else:
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus = df[df['DS_TIPO_CURSO'] == tipo]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
    else:
        if tipo == 'TODOS':
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus=df[df['Campus'] == campus]
                else:
                    df_campus = df[(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
        else:
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
    








    st.divider()           
    st.markdown('## Matrículas por Tipo')
    df_tipo = df_campus.groupby('DS_TIPO_CURSO')['Nome'].count().reset_index()
    fig1 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'DS_TIPO_CURSO'], values='Nome', color='DS_TIPO_CURSO', height=800)
    fig1.data[0].textinfo = 'label+text+value'
    fig1.layout.hovermode = False
    st.plotly_chart(fig1,use_container_width=True)
    
    st.divider()           
    st.markdown('## Matrículas por Eixo')
    df_tipo = df_campus.groupby('DS_EIXO_TECNOLOGICO')['Nome'].count().reset_index()
    fig2 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'DS_EIXO_TECNOLOGICO'], values='Nome', color='DS_EIXO_TECNOLOGICO', height=800)
    fig2.data[0].textinfo = 'label+text+value'
    fig2.layout.hovermode = False
    st.plotly_chart(fig2,use_container_width=True)
    
    st.divider()           
    st.markdown('## Matrículas por Curso')
    df_tipo = df_campus.groupby('NO_CURSO')['Nome'].count().reset_index()
    fig3 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'NO_CURSO'], values='Nome', color='NO_CURSO', height=1600)
    fig3.data[0].textinfo = 'label+text+value'
    fig3.layout.hovermode = False
    st.plotly_chart(fig3,use_container_width=True)
    
def matriculas_equivalentes_por_campus():
    st.markdown('# '+ painel_escolhido)
    
    tipos_de_curso = ['TODOS'] + sorted(df['DS_TIPO_CURSO'].unique())
    eixos_tecnologicos = ['TODOS'] + sorted(df['DS_EIXO_TECNOLOGICO'].unique())
    nomes_de_curso = ['TODOS'] + sorted(df['NO_CURSO'].unique())
    tipo = st.selectbox('Selecione o tipo de curso:', tipos_de_curso)
    if tipo == 'TODOS':
        df_tipo = df
    else:
        df_tipo = df[df['DS_TIPO_CURSO'] == tipo]
        eixos_tecnologicos = ['TODOS'] + sorted(df_tipo['DS_EIXO_TECNOLOGICO'].unique())
    eixo = st.selectbox('Selecione o eixo tecnológico:', eixos_tecnologicos)
    if eixo == 'TODOS':
        df_eixo = df_tipo
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    else:
        df_eixo = df_tipo[df_tipo['DS_EIXO_TECNOLOGICO'] == eixo]
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    curso = st.selectbox('Selecione o curso:', nomes_de_curso)

    if tipo == 'TODOS':
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_figura = df.groupby('Campus')['meq'].count().reset_index()
            else:
                df_campus = df[df['NO_CURSO'] == curso]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
        else:
            if curso == 'TODOS':
                df_campus = df[df['DS_EIXO_TECNOLOGICO'] == eixo]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
            else:
                df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
    else:
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_campus = df[df['DS_TIPO_CURSO'] == tipo]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
            else:
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
        else:
            if curso == 'TODOS':
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()
            else:
                df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
                df_figura = df_campus.groupby('Campus')['meq'].count().reset_index()

    
    fig1 = px.treemap(df_figura, path=[px.Constant('IFPA'), 'Campus'], values='meq', color='Campus', height=800)
    fig1.data[0].textinfo = 'label+text+value'
    fig1.layout.hovermode = False
    fig1.update_traces(texttemplate='%{label} <br> %{value:.2f}')
    st.plotly_chart(fig1,use_container_width=True)

def matriculas_equivalentes_por_tipo_eixo_curso():
    st.markdown('# '+ painel_escolhido)

    lista_de_campus = ['TODOS'] + sorted(df['Campus'].unique())
    tipos_de_curso = ['TODOS'] + sorted(df['DS_TIPO_CURSO'].unique())
    eixos_tecnologicos = ['TODOS'] + sorted(df['DS_EIXO_TECNOLOGICO'].unique())
    nomes_de_curso = ['TODOS'] + sorted(df['NO_CURSO'].unique())
    campus = st.selectbox('Selecione o campus:', lista_de_campus)
    if campus == 'TODOS':
        df_campus = df
    else:
        df_campus = df[df['Campus'] == campus]
    tipo = st.selectbox('Selecione o tipo de curso:', tipos_de_curso)
    if tipo == 'TODOS':
        df_tipo = df_campus
    else:
        df_tipo = df_campus[df_campus['DS_TIPO_CURSO'] == tipo]
        eixos_tecnologicos = ['TODOS'] + sorted(df_tipo['DS_EIXO_TECNOLOGICO'].unique())
    eixo = st.selectbox('Selecione o eixo tecnológico:', eixos_tecnologicos)
    if eixo == 'TODOS':
        df_eixo = df_tipo
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    else:
        df_eixo = df_tipo[df_tipo['DS_EIXO_TECNOLOGICO'] == eixo]
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NO_CURSO'].unique())
    curso = st.selectbox('Selecione o curso:', nomes_de_curso)

    if campus == 'TODOS':
        if tipo == 'TODOS':
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus=df
                else:
                    df_campus = df[df['NO_CURSO'] == curso]
            else:
                if curso == 'TODOS':
                    df_campus = df[df['DS_EIXO_TECNOLOGICO'] == eixo]
                else:
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
        else:
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus = df[df['DS_TIPO_CURSO'] == tipo]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)]
    else:
        if tipo == 'TODOS':
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus=df[df['Campus'] == campus]
                else:
                    df_campus = df[(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
        else:
            if eixo == 'TODOS':
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
            else:
                if curso == 'TODOS':
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['Campus'] == campus)]
                else:
                    df_campus = df[(df['DS_TIPO_CURSO'] == tipo) & (df['DS_EIXO_TECNOLOGICO'] == eixo)&(df['NO_CURSO'] == curso)&(df['Campus'] == campus)]
    
    st.divider()           
    st.markdown('## Matrículas Equivalentes por Tipo')
    df_tipo = df_campus.groupby('DS_TIPO_CURSO')['meq'].sum().reset_index()
    fig1 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'DS_TIPO_CURSO'], values='meq', color='DS_TIPO_CURSO', height=800)
    fig1.data[0].textinfo = 'label+text+value'
    fig1.layout.hovermode = False
    fig1.update_traces(texttemplate='%{label} <br> %{value:.2f}')
    st.plotly_chart(fig1,use_container_width=True)
    
    st.divider()           
    st.markdown('## Matrículas Equivalentes por Eixo')
    df_tipo = df_campus.groupby('DS_EIXO_TECNOLOGICO')['meq'].sum().reset_index()
    fig2 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'DS_EIXO_TECNOLOGICO'], values='meq', color='DS_EIXO_TECNOLOGICO', height=800)
    fig2.data[0].textinfo = 'label+text+value'
    fig2.layout.hovermode = False
    fig2.update_traces(texttemplate='%{label} <br> %{value:.2f}')
    st.plotly_chart(fig2,use_container_width=True)
    
    st.divider()           
    st.markdown('## Matrículas Equivalentes por Curso')
    df_tipo = df_campus.groupby('NO_CURSO')['meq'].sum().reset_index()
    fig3 = px.treemap(df_tipo, path=[px.Constant('IFPA'), 'NO_CURSO'], values='meq', color='NO_CURSO', height=1600)
    fig3.data[0].textinfo = 'label+text+value'
    fig3.layout.hovermode = False
    fig3.update_traces(texttemplate='%{label} <br> %{value:.2f}')
    st.plotly_chart(fig3,use_container_width=True)

def rap():
    st.markdown('# '+ painel_escolhido)
    df_presencial = df[df['Modalidade'] == 'PRESENCIAL']
    meq_rap_por_campus = df.groupby('Campus')['meqrap'].sum().reset_index()
    meq_rap_presencial_por_campus = df_presencial.groupby('Campus')['meqrap'].sum().reset_index()
    rap = meq_rap_por_campus.merge(df_docentes_por_campus, how='left', on='Campus')
    rap_presencial = meq_rap_presencial_por_campus.merge(df_docentes_por_campus, how='left', on='Campus')
    rap['RAP'] = rap['meqrap'] / rap['docentes']
    rap_presencial['RAP'] = rap_presencial['meqrap'] / rap_presencial['docentes']
    rap = rap.sort_values('RAP',ascending=False)
    rap_presencial = rap_presencial.sort_values('RAP',ascending=False)

    matriculas_equivalentes_totais = rap['meqrap'].sum()
    docentes_equivalentes_totais = rap['docentes'].sum()
    rap_total = matriculas_equivalentes_totais / docentes_equivalentes_totais
    matriculas_equivalentes_presenciais_totais = rap_presencial['meqrap'].sum()
    docentes_equivalentes_presenciais_totais = rap_presencial['docentes'].sum()
    rap_presencial_total = matriculas_equivalentes_presenciais_totais / docentes_equivalentes_presenciais_totais
    st.write('**RAP Total**: {:.2f}'.format(rap_total))
    st.write('**RAP Presencial Total**: {:.2f}'.format(rap_presencial_total))
    
    st.divider()

    fig4 = px.bar(rap, x='Campus', y='RAP', color='RAP', title='RAP por Campus')
    fig4.update_layout(showlegend=False)
    fig4.add_hline(y=20.0, line_width=3, line_dash="dash", line_color="green")
    st.plotly_chart(fig4,use_container_width=True)
    
    st.divider()
    
    fig5 = px.bar(rap_presencial, x='Campus', y='RAP', color='RAP', title='RAP presencial por Campus')
    fig5.update_layout(showlegend=False)
    fig5.add_hline(y=20.0, line_width=3, line_dash="dash", line_color="green")
    st.plotly_chart(fig5,use_container_width=True)
    
def eficiencia_academica():
    
    df_eficiencia['DT_DATA_INICIO'] = pd.to_datetime(df_eficiencia['DT_DATA_INICIO'])
    df_eficiencia['DT_DATA_FIM_PREVISTO'] = pd.to_datetime(df_eficiencia['DT_DATA_FIM_PREVISTO'])
    status = df_eficiencia.groupby(['CO_CICLO_MATRICULA','NOME_CURSO','TIPO_CURSO','EIXO_TECNOLOGICO','campus','NO_STATUS_MATRICULA','CO_TIPO_OFERTA_CURSO','DT_DATA_INICIO','DT_DATA_FIM_PREVISTO'])['CO_ALUNO'].count().reset_index()
    status.columns=['Código do ciclo','Nome do Curso','Tipo de Curso','Eixo Tecnológico','Campus','Status','Tipo de Oferta', 'Data de Início', 'Data de Fim Previsto','Quantidade']
    status = status.set_index(['Código do ciclo','Nome do Curso','Tipo de Curso','Eixo Tecnológico','Campus','Status','Tipo de Oferta', 'Data de Início', 'Data de Fim Previsto']).squeeze().unstack('Status').reset_index()
    status = status.fillna(0)
    
    st.markdown('# '+ painel_escolhido)
    
    tipos_de_curso = ['TODOS'] + sorted(df_eficiencia['TIPO_CURSO'].unique())
    eixos_tecnologicos = ['TODOS'] + sorted(df_eficiencia['EIXO_TECNOLOGICO'].unique())
    nomes_de_curso = ['TODOS'] + sorted(df_eficiencia['NOME_CURSO'].unique())
    tipo_de_oferta = ['TODOS','INTEGRADO','SUBSEQUENTE','EJA']
    tipo = st.selectbox('Selecione o tipo de curso:', tipos_de_curso)
    if tipo == 'TODOS':
        df_tipo = df_eficiencia
    else:
        df_tipo = df_eficiencia[df_eficiencia['TIPO_CURSO'] == tipo]
        eixos_tecnologicos = ['TODOS'] + sorted(df_tipo['EIXO_TECNOLOGICO'].unique())
    eixo = st.selectbox('Selecione o eixo tecnológico:', eixos_tecnologicos)
    if eixo == 'TODOS':
        df_eixo = df_tipo
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NOME_CURSO'].unique())
    else:
        df_eixo = df_tipo[df_tipo['EIXO_TECNOLOGICO'] == eixo]
        nomes_de_curso = ['TODOS'] + sorted(df_eixo['NOME_CURSO'].unique())
    curso = st.selectbox('Selecione o curso:', nomes_de_curso)
    tipo_de_oferta = st.selectbox('Selecione o tipo de oferta:', tipo_de_oferta)
    if tipo_de_oferta == 'INTEGRADO':
        codigo_tipo_de_oferta = 1.0
    elif tipo_de_oferta == 'SUBSEQUENTE':
        codigo_tipo_de_oferta = 3.0
    elif tipo_de_oferta == 'EJA':
        codigo_tipo_de_oferta = 2.0
    else:
        codigo_tipo_de_oferta = 0.0

    if tipo == 'TODOS':
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_campus=status
            else:
                df_campus = status[status['Nome do Curso'] == curso]
                
        else:
            if curso == 'TODOS':
                df_campus = status[status['Eixo Tecnológico'] == eixo]
                
            else:
                df_campus = status[(status['Eixo Tecnológico'] == eixo)&(status['Nome do Curso'] == curso)]
                
    else:
        if eixo == 'TODOS':
            if curso == 'TODOS':
                df_campus = status[status['Tipo de Curso'] == tipo]
                
            else:
                df_campus = status[(status['Tipo de Curso'] == tipo)&(status['Nome do Curso'] == curso)]
                
        else:
            if curso == 'TODOS':
                df_campus = status[(status['Tipo de Curso'] == tipo) & (status['Eixo Tecnológico'] == eixo)]
                
            else:
                df_campus = status[(status['Tipo de Curso'] == tipo) & (status['Eixo Tecnológico'] == eixo)&(status['Nome do Curso'] == curso)]
    if codigo_tipo_de_oferta != 0.0:
        df_campus = df_campus[df_campus['Tipo de Oferta'] == codigo_tipo_de_oferta]                

    df_figura = df_campus.groupby('Campus')[['CONCLUIDOS','EM_CURSO','EVADIDOS']].sum().reset_index()
    status2 = df_figura
    
    status2['total']= status2['CONCLUIDOS']+status2['EM_CURSO']+status2['EVADIDOS']
    status2['conc_perc']=status2['CONCLUIDOS']/status2['total']
    status2['ret_perc']=status2['EM_CURSO']/status2['total']
    status2['evad_perc']=status2['EVADIDOS']/status2['total']
    status2['eficiencia'] = status2['conc_perc']+(status2['conc_perc']*status2['ret_perc'])/(status2['conc_perc']+status2['evad_perc'])
    status2 = status2.fillna(0)
    status2['conc_perc'] = round(status2['conc_perc']*100,2)
    status2['ret_perc'] = round(status2['ret_perc']*100,2)
    status2['evad_perc'] = round(status2['evad_perc']*100,2)
    status2['eficiencia'] = round(status2['eficiencia']*100,2)

    status2.columns=['Campus','Concluidos','Em Curso','Evadidos','Total','Conc. (%)','Ret. (%)','Evad. (%)','Eficiência (%)']

    col1,col2,col3 = st.columns([1,1,9])
    concluidos = status2['Concluidos'].sum()
    em_curso = status2['Em Curso'].sum()
    evadidos = status2['Evadidos'].sum()
    total = concluidos + em_curso + evadidos
    conc_perc = concluidos/total
    ret_perc = em_curso/total
    evad_perc = evadidos/total
    eficiencia = conc_perc+(conc_perc*ret_perc)/(conc_perc+evad_perc)
    eficiencia = round(eficiencia*100,2)
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(value=eficiencia, number={"suffix": "%"},title={'text':'TOTAL', 'font':{'family':'Times New Roman','size':48}}))
    col1.plotly_chart(fig6)
    #col1.metric(label="Eficiência Geral", value=eficiencia,border=True)

    fig5 = px.bar(status2, x='Campus', y='Eficiência (%)', color='Campus')
    fig5.update_layout(showlegend=False)
    col3.plotly_chart(fig5,use_container_width=True)
   
    col1,col2,col3 = st.columns([3,7,1])
    col2.dataframe(status2.set_index('Campus'))
    
    st.divider()

    lista_de_campus = ['TODOS'] + sorted(df_eficiencia['campus'].unique())
    campus = st.selectbox('Selecione o campus desejado para detalhar:', lista_de_campus)
    if campus == 'TODOS':
        df_eficiencia_filtrado_por_campus = df_eficiencia
    else:
        df_eficiencia_filtrado_por_campus = df_eficiencia[df_eficiencia['campus'] == campus]
    status3 = df_eficiencia_filtrado_por_campus.groupby(['CO_CICLO_MATRICULA','NOME_CURSO','TIPO_CURSO','EIXO_TECNOLOGICO','campus','NO_STATUS_MATRICULA','CO_TIPO_OFERTA_CURSO','DT_DATA_INICIO','DT_DATA_FIM_PREVISTO'])['CO_ALUNO'].count().reset_index()
    status3.columns=['Código do ciclo','Nome do Curso','Tipo de Curso','Eixo Tecnológico','Campus','Status','Tipo de Oferta', 'Data de Início', 'Data de Fim Previsto','Quantidade']
    status3 = status3.set_index(['Código do ciclo','Nome do Curso','Tipo de Curso','Eixo Tecnológico','Campus','Status','Tipo de Oferta', 'Data de Início', 'Data de Fim Previsto']).squeeze().unstack('Status').reset_index()
    status3 = status3.fillna(0)
    status3['total']= status3['CONCLUIDOS']+status3['EM_CURSO']+status3['EVADIDOS']
    status3['conc_perc']=status3['CONCLUIDOS']/status3['total']
    status3['ret_perc']=status3['EM_CURSO']/status3['total']
    status3['evad_perc']=status3['EVADIDOS']/status3['total']
    status3['eficiencia'] = status3['conc_perc']+(status3['conc_perc']*status3['ret_perc'])/(status3['conc_perc']+status3['evad_perc'])
    status3 = status3.fillna(0)
    status3['conc_perc'] = round(status3['conc_perc']*100,2)
    status3['ret_perc'] = round(status3['ret_perc']*100,2)
    status3['evad_perc'] = round(status3['evad_perc']*100,2)
    status3['eficiencia'] = round(status3['eficiencia']*100,2)
    status3 = status3.set_index('Código do ciclo')
    status3=status3[['Nome do Curso','Tipo de Curso','Eixo Tecnológico','Data de Início','Data de Fim Previsto','CONCLUIDOS','EM_CURSO','EVADIDOS','total','conc_perc','ret_perc','evad_perc','eficiencia']]
    status3.columns=['Nome do Curso','Tipo de Curso','Eixo Tecnológico','Data de Início','Data de Fim Previsto','Concluidos','Em Curso','Evadidos','Total','Conc. (%)','Ret. (%)','Evad. (%)','Eficiência (%)']
    st.dataframe(status3)
    
    #df_figura = df_eficiencia_filtrado_por_campus.groupby(['DT_DATA_INICIO','DT_DATA_FIM_PREVISTO'])[['CONCLUIDOS','EM_CURSO','EVADIDOS']].sum().reset_index()
    #df_figura



page_names_to_funcs = {
    'Matrículas por campus': matriculas_por_campus,
    'Matrículas por tipo, eixo e curso': matriculas_por_tipo_eixo_curso,
    'Matrículas equivalentes por campus': matriculas_equivalentes_por_campus,
    'Matrículas equivalentes por tipo, eixo e curso': matriculas_equivalentes_por_tipo_eixo_curso,
    'RAP': rap,
    'Eficiência Acadêmica': eficiencia_academica
}

page_names_to_funcs[painel_escolhido]()




