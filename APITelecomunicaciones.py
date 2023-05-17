import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import glob
import re
import os
from urllib.request import urlopen
import json
from streamlit_folium import folium_static
from st_aggrid import AgGrid
import geopandas as gpd
import folium
from folium.plugins import FloatImage
import urllib
from functools import partial, reduce
import time
import requests
from bs4 import BeautifulSoup

LogoComision="data:image/png;base64,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"
LogoComision2="https://postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

st.set_page_config(
    page_title="API Telecomunicaciones", page_icon=LogoComision,layout="wide",initial_sidebar_state="expanded")  

st.markdown("""<style type="text/css">
    h1{ 
        background: linear-gradient(to bottom, #FA7268, #8E2800);
        text-align: center;
        padding: 15px;
        font-family: sans-serif;
        font-size:1.60rem;
        color: white;
        width:100%;
        z-index:9999;
        top:0px;
        left:0;
    }
    .e8zbici0 {display:none}
    .e8zbici2 {display:none}
    .e16nr0p31 {display:none}
    .barra-superior{top: 0;
        position: fixed;
        background-color: #27348b;
        width: 100%;
        color:white;
        z-index: 999;
        height: 80px;
        left: 0px;
        text-align: center;
        padding: 0px;
        font-size: 36px;
        font-weight: 700;
    }
    .css-y3whyl, .css-xqnn38 {background-color:#ccc}
    .css-1uvyptr:hover,.css-1uvyptr {background: #ccc}
    .block-container {padding-top:0;}
    .css-k0sv6k {height:0rem}
    .e1tzin5v3 {text-align: center}
    h2{
        background: #fffdf7;
        text-align: center;
        padding: 50px;
        text-decoration: underline;
        text-decoration-style: double;
        color: #27348b;}
    h3{ 
        background: linear-gradient(to bottom, #2e297b, #4ab4e8);
        text-align: center;
        padding: 15px;
        font-family: sans-serif;
        font-size:1.30rem;
        color: white;
        width:100%;
        z-index:9999;
        top:0px;
        left:0;
        }

    .imagen-flotar{float:left;}
    @media (max-width:1230px){
        .barra-superior{height:160px;} 
        .main, .css-1lcbmhc > div{margin-top:215px;}
        .imagen-flotar{float:none}
        h1{top:160px;}
        }        
    </style>""", unsafe_allow_html=True)  

st.markdown("# <center>API Mercados TIC</center>",unsafe_allow_html=True)
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')
#Función para obtener los nombres de todas las columnas disponibles 
def GetAllColumns(resourceid):
    consulta='https://www.postdata.gov.co/api/action/datastore/search.json?resource_id=' + resourceid
    response = urlopen(consulta) 
    json_data = json.loads(response.read())
    fields = json_data["result"]["fields"]
    columns = []
    for field in fields:
        column_name = field["id"]
        if column_name != "entry_id":
            columns.append(column_name)
    return columns
    
def API(resourceid,columns_fields,columns,filters,metric,grouping_col):
    DF = pd.DataFrame()
    consulta='https://www.postdata.gov.co/api/action/datastore/search.json?resource_id=' + resourceid + ''\
             +filters\
             +columns_fields\
             +'&group_by='+columns\
             +'&'+metric+'='+grouping_col 
    response_base = urlopen(consulta.replace(" ", "%20")+ '&limit=10000000') 
    json_base = json.loads(response_base.read())
    df = pd.DataFrame(json_base['result']['records'])
    DF = pd.concat([DF, df], ignore_index=True)
    return DF    

url_dict={'susIntfijo':"https://postdata.gov.co/dataset/suscriptores-e-ingresos-de-internet-fijo/resource/34bbf5b5-0537-4bf0-8836-3f51d1a24162#{}",
'ingIntfijo':"https://postdata.gov.co/dataset/suscriptores-e-ingresos-de-internet-fijo/resource/d917a68d-9cb9-4257-82f1-74115a4cf629#{}",
'velIntfijo':"https://postdata.gov.co/dataset/suscriptores-e-ingresos-de-internet-fijo/resource/864bacb8-b2a2-4cd1-9064-d67850e767b3#{}",
         'aboIntmovilDDA':"https://www.postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-demanda/resource/3df620f6-deec-42a0-a6af#{}",
         'ingIntmovilDDA':"https://www.postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-demanda/resource/60a55889-ba71-45ff-b68f#{}",
         'trafIntmovilDDA':"https://www.postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-demanda/resource/c0be7034-29f8-4400-be54#{}",
         'susIntmovilCF':"https://www.postdata.gov.co/dataset/suscriptores-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-cargo-fijo/resource/47d07e20-b257-4aaf#{}",
         'ingIntmovilCF':"https://www.postdata.gov.co/dataset/suscriptores-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-cargo-fijo/resource/8366e39c-6a14-483a#{}",
         'trafIntmovilCF':"https://www.postdata.gov.co/dataset/suscriptores-ingresos-y-tr%C3%A1fico-de-internet-m%C3%B3vil-por-cargo-fijo/resource/d40c5e75-db56-4ec1#{}",
         'aboTelmovil':"https://postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-telefon%C3%ADa-m%C3%B3vil/resource/3a9c0304-3795-4c55-a78e-079362373b4d#{}",
         'ingTelmovil':"https://postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-telefon%C3%ADa-m%C3%B3vil/resource/43f0d3a9-cd5c-4f22-a996-74eae6cba9a3#{}",
         'trafTelmovil':"https://postdata.gov.co/dataset/abonados-ingresos-y-tr%C3%A1fico-de-telefon%C3%ADa-m%C3%B3vil/resource/1384a4d4-42d7-4930-b43c-bf9768c47ccb#{}",
         'linTelfija':"https://postdata.gov.co/dataset/telefon%C3%ADa-local/resource/967fbbd1-1c10-42b8-a6af-88b2376d43e7#{}",
         'ingTelfija':"https://postdata.gov.co/dataset/telefon%C3%ADa-fija/resource/8b0fc631-461c-4a09-bb86-b5d591265e71#{}",
         'susTVporsus':"https://postdata.gov.co/dataset/suscriptores-e-ingresos-de-televisi%C3%B3n-por-suscripci%C3%B3n/resource/0c4b69a7-734d-432c-9d9b#{}",
         'ingTVporsus':"https://postdata.gov.co/dataset/suscriptores-e-ingresos-de-televisi%C3%B3n-por-suscripci%C3%B3n/resource/1033b0f2-8107-4e04-ae33#{}"}
node_dict={'susIntfijo':'614','ingIntfijo':'220','velIntfijo':'598','aboIntmovilDDA':'228','ingIntmovilDDA':'230',
          'trafIntmovilDDA':'232','susIntmovilCF':'224','ingIntmovilCF':'222','trafIntmovilCF':'226','aboTelmovil':'234',
          'ingTelmovil':'236','trafTelmovil':'238','linTelfija':'166','ingTelfija':'549','susTVporsus':'282',
          'ingTVporsus':'283'}
          
def columns_dict(x):
    response = requests.get(url_dict[x])
    soup = BeautifulSoup(response.content, 'html.parser')
    table = str(soup.find('table', {'id': 'tablefield-node-'+node_dict[x]+'-field_dictionary-0'}))
    cols=[col.lower() for col in pd.read_html(table)[0]['CAMPO'].values.tolist()]
    return cols
     
select_servicio=st.radio('Seleccione el servicio',['Internet fijo','Internet móvil','Telefonía móvil','Telefonía fija','TV por suscripción'],horizontal=True)
Agroup_metric={'Suma':'sum','Promedio':'avg','Mínimo':'min','Máximo':'max','Desviación estándar':'std','Varianza':'variance','Conteo':'count'}

if select_servicio=='Internet fijo':
    st.markdown("### <center>Internet fijo</center>",unsafe_allow_html=True)
    select_dimen=st.selectbox('Escoja la variable',['Accesos','Ingresos','Velocidades'])
    
    if select_dimen=='Accesos':
        st.markdown("#### <center>Accesos</center>",unsafe_allow_html=True)
        id_accesos_Intfijo='34bbf5b5-0537-4bf0-8836-3f51d1a24162'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupACCIntfijo=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_accesos_Intfijo))
        with col2:
            position_acc=[i for i, item in enumerate(GetAllColumns(id_accesos_Intfijo)) if re.search(re.compile("acc"), item)][0]
            valagrupACCIntfijo=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_accesos_Intfijo),position_acc)
        columnsagrupACCIntfijo_len = len(columnsagrupACCIntfijo)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupACCIntfijo:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupACCIntfijo])       
        Filtros_IntFijoAcc=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')

        if Filtros_IntFijoAcc==True and columnsagrupACCIntfijo_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupACCIntfijo)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupACCIntfijo[i])
                    values[columnsagrupACCIntfijo[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DFIntFijoAcc=st.button('Generar base de datos')   
        
        if  columnsagrupACCIntfijo_len!=0 and DFIntFijoAcc==True:
            AccIntFijo=API(id_accesos_Intfijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupACCIntfijo)  
            if AccIntFijo.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(AccIntFijo,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(AccIntFijo),file_name='Accesos_IntFijo.csv',mime='text/csv')   
                
        cols_accIntfijo=columns_dict('susIntfijo')
        diff_cols_accIntfijo=list(set(GetAllColumns(id_accesos_Intfijo))^set(cols_accIntfijo))
        if len(diff_cols_accIntfijo)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_accIntfijo)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')
                
    elif select_dimen=='Ingresos':     
        st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
        id_ingresos_Intfijo='d917a68d-9cb9-4257-82f1-74115a4cf629'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupINGIntfijo=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_Intfijo))
        with col2:
            position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_Intfijo)) if re.search(re.compile("ingreso"), item)][0]
            valagrupINGIntfijo=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_Intfijo),position_ing)
        columnsagrupINGIntfijo_len = len(columnsagrupINGIntfijo)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupINGIntfijo:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupINGIntfijo])       
        Filtros_IntFijoING=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_IntFijoING==True and columnsagrupINGIntfijo_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupINGIntfijo)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupINGIntfijo[i])
                    values[columnsagrupINGIntfijo[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DFIntFijoING=st.button('Generar base de datos')   
        
        if  columnsagrupINGIntfijo_len!=0 and DFIntFijoING==True:
            INGIntFijo=API(id_ingresos_Intfijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupINGIntfijo)  
            if INGIntFijo.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(INGIntFijo,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(INGIntFijo),file_name='Ingresos_IntFijo.csv',mime='text/csv')        

        cols_ingIntfijo=columns_dict('ingIntfijo')
        diff_cols_ingIntfijo=list(set(GetAllColumns(id_ingresos_Intfijo))^set(cols_ingIntfijo))
        if len(diff_cols_ingIntfijo)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_ingIntfijo)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')

    elif select_dimen=='Velocidades':     
        st.markdown("#### <center>Velocidades</center>",unsafe_allow_html=True)
        id_velocidades_Intfijo='864bacb8-b2a2-4cd1-9064-d67850e767b3'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupVelIntfijo=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_velocidades_Intfijo))
        with col2:
            position_vel=[i for i, item in enumerate(GetAllColumns(id_velocidades_Intfijo)) if re.search(re.compile("velocidad"), item)][0]
            valagrupVelIntfijo=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_velocidades_Intfijo),position_vel)
        columnsagrupVelIntfijo_len = len(columnsagrupVelIntfijo)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupVelIntfijo:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupVelIntfijo])       
        Filtros_IntFijoVel=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_IntFijoVel==True and columnsagrupVelIntfijo_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupVelIntfijo)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupVelIntfijo[i])
                    values[columnsagrupVelIntfijo[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],1)
        DFIntFijoVel=st.button('Generar base de datos')   
        
        if  columnsagrupVelIntfijo_len!=0 and DFIntFijoVel==True:
            VelIntFijo=API(id_velocidades_Intfijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupVelIntfijo)  
            if VelIntFijo.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(VelIntFijo,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(VelIntFijo),file_name='Velocidades_IntFijo.csv',mime='text/csv')        

        cols_velIntfijo=columns_dict('velIntfijo')
        diff_cols_velIntfijo=list(set(GetAllColumns(id_velocidades_Intfijo))^set(cols_velIntfijo))
        if len(diff_cols_velIntfijo)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_velIntfijo)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')
       
elif select_servicio=='Internet móvil':
    st.markdown("### <center>Internet movil</center>",unsafe_allow_html=True)     
    select_agrupIntmovil=st.radio('',['Demanda', 'Cargo Fijo'], horizontal=True)    
    
    if select_agrupIntmovil=='Demanda':
        select_dimen=st.selectbox('Escoja la variable',['Abonados','Ingresos','Tráfico'])
        
        if select_dimen=='Abonados':
            st.markdown("#### <center>Abonados</center>",unsafe_allow_html=True)
            id_abonados_IntmovilDemanda='3df620f6-deec-42a0-a6af-44ca23c2b73c'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupAboIntmovilDDA=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_abonados_IntmovilDemanda))
            with col2:
                position_abo=[i for i, item in enumerate(GetAllColumns(id_abonados_IntmovilDemanda)) if re.search(re.compile("abona"), item)][0]
                valagrupAboIntmovilDem=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_abonados_IntmovilDemanda),position_abo)
            columnsagrupAboIntmovilDDA_len = len(columnsagrupAboIntmovilDDA)    
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupAboIntmovilDDA:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupAboIntmovilDDA])       
            Filtros_IntmovilAboDDA=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilAboDDA==True and columnsagrupAboIntmovilDDA_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupAboIntmovilDDA)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupAboIntmovilDDA[i])
                        values[columnsagrupAboIntmovilDDA[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DFIntmovilAboDDA=st.button('Generar base de datos')   
            
            if  columnsagrupAboIntmovilDDA_len!=0 and DFIntmovilAboDDA==True:
                AboIntMovilDDA=API(id_abonados_IntmovilDemanda,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupAboIntmovilDem)  
                if AboIntMovilDDA.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(AboIntMovilDDA,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(AboIntMovilDDA),file_name='Abonados_IntMovil_Demanda.csv',mime='text/csv')        

            cols_aboIntmovilDDA=columns_dict('aboIntmovilDDA')
            diff_cols_aboIntmovilDDA=list(set(GetAllColumns(id_abonados_IntmovilDemanda))^set(cols_aboIntmovilDDA))
            if len(diff_cols_aboIntmovilDDA)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.')
                st.markdown(diff_cols_aboIntmovilDDA)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')

        elif select_dimen=='Ingresos':
            st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
            id_ingresos_IntmovilDemanda='60a55889-ba71-45ff-b68f-33b503da36f2'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupIngIntmovilDDA=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_IntmovilDemanda))
            with col2:
                position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_IntmovilDemanda)) if re.search(re.compile("ingreso"), item)][0]
                valagrupIngIntmovilDem=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_IntmovilDemanda),position_ing)
            columnsagrupIngIntmovilDDA_len = len(columnsagrupIngIntmovilDDA)    
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupIngIntmovilDDA:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupIngIntmovilDDA])       
            Filtros_IntmovilIngDDA=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilIngDDA==True and columnsagrupIngIntmovilDDA_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupIngIntmovilDDA)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupIngIntmovilDDA[i])
                        values[columnsagrupIngIntmovilDDA[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DFIntmovilIngDDA=st.button('Generar base de datos')   
            
            if  columnsagrupIngIntmovilDDA_len!=0 and DFIntmovilIngDDA==True:
                IngIntMovilDDA=API(id_ingresos_IntmovilDemanda,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupIngIntmovilDem)  
                if IngIntMovilDDA.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(IngIntMovilDDA,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(IngIntMovilDDA),file_name='Ingresos_IntMovil_Demanda.csv',mime='text/csv')              

            cols_ingIntmovilDDA=columns_dict('ingIntmovilDDA')
            diff_cols_ingIntmovilDDA=list(set(GetAllColumns(id_ingresos_IntmovilDemanda))^set(cols_ingIntmovilDDA))
            if len(diff_cols_ingIntmovilDDA)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
                st.markdown(diff_cols_ingIntmovilDDA)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')

        elif select_dimen=='Tráfico':
            st.markdown("#### <center>Tráfico</center>",unsafe_allow_html=True)
            id_trafico_IntmovilDemanda='c0be7034-29f8-4400-be54-c4aafe5df606'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupTrafIntmovilDDA=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_trafico_IntmovilDemanda))
            with col2:
                position_traf=[i for i, item in enumerate(GetAllColumns(id_trafico_IntmovilDemanda)) if re.search(re.compile("trafico"), item)][0]
                valagrupTrafIntmovilDem=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_trafico_IntmovilDemanda),position_traf)
            columnsagrupTrafIntmovilDDA_len = len(columnsagrupTrafIntmovilDDA)
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupTrafIntmovilDDA:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupTrafIntmovilDDA])       
            Filtros_IntmovilTrafDDA=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilTrafDDA==True and columnsagrupTrafIntmovilDDA_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupTrafIntmovilDDA)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupTrafIntmovilDDA[i])
                        values[columnsagrupTrafIntmovilDDA[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DFIntmovilTrafDDA=st.button('Generar base de datos')   
            
            if  columnsagrupTrafIntmovilDDA_len!=0 and DFIntmovilTrafDDA==True:
                TrafIntMovilDDA=API(id_trafico_IntmovilDemanda,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupTrafIntmovilDem)  
                if TrafIntMovilDDA.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(TrafIntMovilDDA,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(TrafIntMovilDDA),file_name='Trafico_IntMovil_Demanda.csv',mime='text/csv')                                  

            cols_trafIntmovilDDA=columns_dict('trafIntmovilDDA')
            diff_cols_trafIntmovilDDA=list(set(GetAllColumns(id_trafico_IntmovilDemanda))^set(cols_trafIntmovilDDA))
            if len(diff_cols_trafIntmovilDDA)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
                st.markdown(diff_cols_trafIntmovilDDA)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')

    if select_agrupIntmovil=='Cargo Fijo': 
        select_dimen=st.selectbox('Escoja la variable',['Suscriptores','Ingresos','Tráfico'])

        if select_dimen=='Suscriptores':
            st.markdown("#### <center>Suscriptores</center>",unsafe_allow_html=True)
            id_suscriptores_IntmovilCargoFijo='47d07e20-b257-4aaf-9309-1501c75a826c'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupSusIntmovilCF=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_suscriptores_IntmovilCargoFijo))
            with col2:
                position_sus=[i for i, item in enumerate(GetAllColumns(id_suscriptores_IntmovilCargoFijo)) if re.search(re.compile("susc"), item)][0]
                valagrupSusIntmovilCF=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_suscriptores_IntmovilCargoFijo),position_sus)
            columnsagrupSusIntmovilCF_len = len(columnsagrupSusIntmovilCF)    
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupSusIntmovilCF:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupSusIntmovilCF])       
            Filtros_IntmovilSusCF=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilSusCF==True and columnsagrupSusIntmovilCF_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupSusIntmovilCF)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupSusIntmovilCF[i])
                        values[columnsagrupSusIntmovilCF[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DF=st.button('Generar base de datos')   
            columnsagrupSusIntmovilCF_len = len(columnsagrupSusIntmovilCF)
            if  columnsagrupSusIntmovilCF_len!=0 and DF==True:
                SusIntMovilCF=API(id_suscriptores_IntmovilCargoFijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupSusIntmovilCF)  
                if SusIntMovilCF.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(SusIntMovilCF,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(SusIntMovilCF),file_name='Suscriptores_IntMovil_CargoFijo.csv',mime='text/csv')        

            cols_susIntmovilCF=columns_dict('susIntmovilCF')
            diff_cols_susIntmovilCF=list(set(GetAllColumns(id_suscriptores_IntmovilCargoFijo))^set(cols_susIntmovilCF))
            if len(diff_cols_susIntmovilCF)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
                st.markdown(diff_cols_susIntmovilCF)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')
    
        if select_dimen=='Ingresos':
            st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
            id_ingresos_IntmovilCargoFijo='8366e39c-6a14-483a-80f4-7278ceb39f88'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupIngIntmovilCF=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_IntmovilCargoFijo))
            with col2:
                position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_IntmovilCargoFijo)) if re.search(re.compile("ingreso"), item)][0]
                valagrupIngIntmovilCF=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_IntmovilCargoFijo),position_ing)
            columnsagrupIngIntmovilCF_len = len(columnsagrupIngIntmovilCF)    
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupIngIntmovilCF:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupIngIntmovilCF])       
            Filtros_IntmovilIngCF=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilIngCF==True and columnsagrupIngIntmovilCF_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupIngIntmovilCF)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupIngIntmovilCF[i])
                        values[columnsagrupIngIntmovilCF[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DF=st.button('Generar base de datos')   
            columnsagrupIngIntmovilCF_len = len(columnsagrupIngIntmovilCF)
            if  columnsagrupIngIntmovilCF_len!=0 and DF==True:
                IngIntMovilCF=API(id_ingresos_IntmovilCargoFijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupIngIntmovilCF)  
                if IngIntMovilCF.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(IngIntMovilCF,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(IngIntMovilCF),file_name='Ingresos_IntMovil_CargoFijo.csv',mime='text/csv')      

            cols_ingIntmovilCF=columns_dict('ingIntmovilCF')
            diff_cols_ingIntmovilCF=list(set(GetAllColumns(id_ingresos_IntmovilCargoFijo))^set(cols_ingIntmovilCF))
            if len(diff_cols_ingIntmovilCF)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
                st.markdown(diff_cols_ingIntmovilCF)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')

        if select_dimen=='Tráfico':
            st.markdown("#### <center>Tráfico</center>",unsafe_allow_html=True)
            id_trafico_IntmovilCargoFijo='d40c5e75-db56-4ec1-a441-0314c47bd71d'
            col1,col2=st.columns(2)
            with col1:
                columnsagrupTrafIntmovilCF=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_trafico_IntmovilCargoFijo))
            with col2:
                position_traf=[i for i, item in enumerate(GetAllColumns(id_trafico_IntmovilCargoFijo)) if re.search(re.compile("traf"), item)][0]
                valagrupTrafIntmovilCF=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_trafico_IntmovilCargoFijo),position_traf)
            columnsagrupTrafIntmovilCF_len = len(columnsagrupTrafIntmovilCF)    
            filter_string = ''
            fields_str = "&fields[]="
            for column in columnsagrupTrafIntmovilCF:
                fields_str += column + "&fields[]="
            fields_str = fields_str[:-10]       
            columns_groupby_API=','.join([str(col) for col in columnsagrupTrafIntmovilCF])       
            Filtros_IntmovilTrafCF=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
            if Filtros_IntmovilTrafCF==True and columnsagrupTrafIntmovilCF_len!=0:
                st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
                num_cols = len(columnsagrupTrafIntmovilCF)
                col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
                code = f"{col_vars}=st.columns({num_cols})"
                exec(code)
                values = {}
                for i, column_var in enumerate(eval(f'({col_vars})')):
                    with column_var:
                        text_input = st.text_input(columnsagrupTrafIntmovilCF[i])
                        values[columnsagrupTrafIntmovilCF[i]] = text_input
                filters = {}
                for key, val in values.items():
                    if val:
                        filters[f'filters[{key}]'] = ','.join(val.split(','))            
                for key, val in filters.items():
                    filter_string += f'&{key}={val}'   
      
            agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
            DF=st.button('Generar base de datos')   
            
            if  columnsagrupTrafIntmovilCF_len!=0 and DF==True:
                TrafIntMovilCF=API(id_trafico_IntmovilCargoFijo,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupTrafIntmovilCF)  
                if TrafIntMovilCF.empty==True:
                    st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
                else:
                    progress_bar = st.progress(0)
                    for i in range(1, 101):
                        progress_bar.progress(i)                        
                    AgGrid(TrafIntMovilCF,width_mode='fit_columns')
                    st.download_button(label="Descargar CSV",data=convert_df(TrafIntMovilCF),file_name='Trafico_IntMovil_CargoFijo.csv',mime='text/csv')                          

            cols_trafIntmovilCF=columns_dict('trafIntmovilCF')
            diff_cols_trafIntmovilCF=list(set(GetAllColumns(id_trafico_IntmovilCargoFijo))^set(cols_trafIntmovilCF))
            if len(diff_cols_trafIntmovilCF)!=0:
                st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
                st.markdown(diff_cols_trafIntmovilCF)
            else:    
                st.success('Toda las columnas de la base coinciden con su diccionario.')
                                        
elif select_servicio=='Telefonía móvil':   
    st.markdown("### <center>Telefonía movil</center>",unsafe_allow_html=True)    
    select_dimen=st.selectbox('Escoja la variable',['Abonados','Ingresos','Tráfico'])
    
    if select_dimen=='Abonados':
        st.markdown("#### <center>Abonados</center>",unsafe_allow_html=True)
        id_abonados_TelMovil='3a9c0304-3795-4c55-a78e-079362373b4d'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupAboTelMovil=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_abonados_TelMovil))
        with col2:
            position_abo=[i for i, item in enumerate(GetAllColumns(id_abonados_TelMovil)) if re.search(re.compile("abona"), item)][0]
            valagrupAboTelMovil=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_abonados_TelMovil),position_abo)
        columnsagrupAboTelMovil_len = len(columnsagrupAboTelMovil)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupAboTelMovil:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupAboTelMovil])       
        Filtros_TelMovil=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_TelMovil==True and columnsagrupAboTelMovil_len:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupAboTelMovil)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupAboTelMovil[i])
                    values[columnsagrupAboTelMovil[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupAboTelMovil_len!=0 and DF==True:
            AboTelMovil=API(id_abonados_TelMovil,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupAboTelMovil)  
            if AboTelMovil.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(AboTelMovil,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(AboTelMovil),file_name='Abonados_TelMovil.csv',mime='text/csv')        

        cols_aboTelmovil=columns_dict('aboTelmovil')
        diff_cols_aboTelmovil=list(set(GetAllColumns(id_abonados_TelMovil))^set(cols_aboTelmovil))
        if len(diff_cols_aboTelmovil)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_aboTelmovil)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')

    if select_dimen=='Ingresos':
        st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
        id_ingresos_TelMovil='43f0d3a9-cd5c-4f22-a996-74eae6cba9a3'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupIngTelMovil=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_TelMovil))
        with col2:
            position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_TelMovil)) if re.search(re.compile("ingreso"), item)][0]
            valagrupIngTelMovil=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_TelMovil),position_ing)
        columnsagrupIngTelMovil_len = len(columnsagrupIngTelMovil)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupIngTelMovil:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupIngTelMovil])       
        Filtros_IngTelMovil=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_IngTelMovil==True and columnsagrupIngTelMovil_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupIngTelMovil)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupIngTelMovil[i])
                    values[columnsagrupIngTelMovil[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupIngTelMovil_len!=0 and DF==True:
            IngTelMovil=API(id_ingresos_TelMovil,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupIngTelMovil)  
            if IngTelMovil.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(IngTelMovil,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(IngTelMovil),file_name='Ingresos_TelMovil.csv',mime='text/csv')         

        cols_ingTelmovil=columns_dict('ingTelmovil')
        diff_cols_ingTelmovil=list(set(GetAllColumns(id_ingresos_TelMovil))^set(cols_ingTelmovil))
        if len(diff_cols_ingTelmovil)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_ingTelmovil)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')

    if select_dimen=='Tráfico':
        st.markdown("#### <center>Tráfico</center>",unsafe_allow_html=True)
        id_trafico_TelMovil='1384a4d4-42d7-4930-b43c-bf9768c47ccb'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupTrafTelMovil=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_trafico_TelMovil))
        with col2:
            position_traf=[i for i, item in enumerate(GetAllColumns(id_trafico_TelMovil)) if re.search(r'\b(?!id|tipo)\w*trafico\w*\b', item)][0]
            valagrupTrafTelMovil=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_trafico_TelMovil),position_traf)
        columnsagrupTrafTelMovil_len = len(columnsagrupTrafTelMovil)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupTrafTelMovil:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupTrafTelMovil])       
        Filtros_TrafTelMovil=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_TrafTelMovil==True and columnsagrupTrafTelMovil_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupTrafTelMovil)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupTrafTelMovil[i])
                    values[columnsagrupTrafTelMovil[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupTrafTelMovil_len!=0 and DF==True:
            TrafTelMovil=API(id_trafico_TelMovil,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupTrafTelMovil)  
            if TrafTelMovil.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(TrafTelMovil,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(TrafTelMovil),file_name='Trafico_TelMovil.csv',mime='text/csv')  

        cols_trafTelmovil=columns_dict('trafTelmovil')
        diff_cols_trafTelmovil=list(set(GetAllColumns(id_trafico_TelMovil))^set(cols_trafTelmovil))
        if len(diff_cols_trafTelmovil)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_trafTelmovil)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')

elif select_servicio=='Telefonía fija':   
    st.markdown("### <center>Telefonía fija</center>",unsafe_allow_html=True)    
    select_dimen=st.selectbox('Escoja la variable',['Líneas','Ingresos'])   

    if select_dimen=='Líneas':
        st.markdown("#### <center>Líneas</center>",unsafe_allow_html=True)
        id_lineas_TelLocal='967fbbd1-1c10-42b8-a6af-88b2376d43e7'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupLinTelLocal=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_lineas_TelLocal))
        with col2:
            position_lin=[i for i, item in enumerate(GetAllColumns(id_lineas_TelLocal)) if re.search(re.compile("linea"), item)][0]
            valagrupLinTelLocal=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_lineas_TelLocal),position_lin)
        columnsagrupLinTelLocal_len = len(columnsagrupLinTelLocal)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupLinTelLocal:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupLinTelLocal])       
        Filtros_LinTelLocal=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_LinTelLocal==True and columnsagrupLinTelLocal_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupLinTelLocal)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupLinTelLocal[i])
                    values[columnsagrupLinTelLocal[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupLinTelLocal_len!=0 and DF==True:
            LinTelLocal=API(id_lineas_TelLocal,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupLinTelLocal)  
            if LinTelLocal.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(LinTelLocal,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(LinTelLocal),file_name='Lineas_TelLocal.csv',mime='text/csv')        

        cols_linTelfija=columns_dict('linTelfija')
        diff_cols_linTelfija=list(set(GetAllColumns(id_lineas_TelLocal))^set(cols_linTelfija))
        if len(diff_cols_linTelfija)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_linTelfija)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')
        
    if select_dimen=='Ingresos':
        st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
        id_ingresos_TelLocal='8b0fc631-461c-4a09-bb86-b5d591265e71'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupIngTelLocal=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_TelLocal))
        with col2:
            position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_TelLocal)) if re.search(re.compile("ingreso"), item)][0]
            valagrupIngTelLocal=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_TelLocal),position_ing)
        columnsagrupIngTelLocal_len = len(columnsagrupIngTelLocal)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupIngTelLocal:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupIngTelLocal])       
        Filtros_LinTelLocal=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_LinTelLocal==True and columnsagrupIngTelLocal_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupIngTelLocal)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupIngTelLocal[i])
                    values[columnsagrupIngTelLocal[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupIngTelLocal_len!=0 and DF==True:
            IngTelLocal=API(id_ingresos_TelLocal,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupIngTelLocal)  
            if IngTelLocal.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(IngTelLocal,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(IngTelLocal),file_name='Ingresos_TelLocal.csv',mime='text/csv')            

        cols_ingTelfija=columns_dict('ingTelfija')
        diff_cols_ingTelfija=list(set(GetAllColumns(id_ingresos_TelLocal))^set(cols_ingTelfija))
        if len(diff_cols_ingTelfija)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_ingTelfija)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')
                
elif select_servicio=='TV por suscripción':   
    st.markdown("### <center>Televisión por suscripción</center>",unsafe_allow_html=True)    
    select_dimen=st.selectbox('Escoja la variable',['Suscriptores','Ingresos'])       
    
    if select_dimen=='Suscriptores':
        st.markdown("#### <center>Suscriptores</center>",unsafe_allow_html=True)
        id_suscriptores_TVporSus='0c4b69a7-734d-432c-9d9b-9dc600d50391'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupSusTvporSus=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_suscriptores_TVporSus))
        with col2:
            position_sus=[i for i, item in enumerate(GetAllColumns(id_suscriptores_TVporSus)) if re.search(re.compile("suscrip"), item)][0]
            valagrupSusTVporSus=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_suscriptores_TVporSus),position_sus)
        columnsagrupSusTvporSus_len = len(columnsagrupSusTvporSus)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupSusTvporSus:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupSusTvporSus])       
        Filtros_SusTVporSus=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_SusTVporSus==True and columnsagrupSusTvporSus_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupSusTvporSus)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupSusTvporSus[i])
                    values[columnsagrupSusTvporSus[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupSusTvporSus_len!=0 and DF==True:
            SusTVporSus=API(id_suscriptores_TVporSus,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupSusTVporSus)  
            if SusTVporSus.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(SusTVporSus,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(SusTVporSus),file_name='Suscriptores_TV_Suscripcion.csv',mime='text/csv')        

        cols_susTVporsus=columns_dict('susTVporsus')
        diff_cols_susTVporsus=list(set(GetAllColumns(id_suscriptores_TVporSus))^set(cols_susTVporsus))
        if len(diff_cols_susTVporsus)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_susTVporsus)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')

    if select_dimen=='Ingresos':
        st.markdown("#### <center>Ingresos</center>",unsafe_allow_html=True)
        id_ingresos_TVporSus='1033b0f2-8107-4e04-ae33-8b12882b762d'
        col1,col2=st.columns(2)
        with col1:
            columnsagrupIngTvporSus=st.multiselect('Escoja las columnas de su interes para obtener la base de datos, sin seleccionar el campo a agrupar.',GetAllColumns(id_ingresos_TVporSus))
        with col2:
            position_ing=[i for i, item in enumerate(GetAllColumns(id_ingresos_TVporSus)) if re.search(re.compile("ingreso"), item)][0]
            valagrupIngTVporSus=st.selectbox('Escoja la columna de agrupación',GetAllColumns(id_ingresos_TVporSus),position_ing)
        columnsagrupIngTvporSus_len = len(columnsagrupIngTvporSus)    
        filter_string = ''
        fields_str = "&fields[]="
        for column in columnsagrupIngTvporSus:
            fields_str += column + "&fields[]="
        fields_str = fields_str[:-10]       
        columns_groupby_API=','.join([str(col) for col in columnsagrupIngTvporSus])       
        Filtros_IngTVporSus=st.checkbox('¿Desea añadir filtros en algunas de las columnas seleccionadas?')
        if Filtros_IngTVporSus==True and columnsagrupIngTvporSus_len!=0:
            st.markdown('Escriba los valores a añadir en los filtros separados por coma. Ej: 2018,2019,2021,2022')
            num_cols = len(columnsagrupIngTvporSus)
            col_vars = ','.join([f'col{i+1}' for i in range(num_cols)])
            code = f"{col_vars}=st.columns({num_cols})"
            exec(code)
            values = {}
            for i, column_var in enumerate(eval(f'({col_vars})')):
                with column_var:
                    text_input = st.text_input(columnsagrupIngTvporSus[i])
                    values[columnsagrupIngTvporSus[i]] = text_input
            filters = {}
            for key, val in values.items():
                if val:
                    filters[f'filters[{key}]'] = ','.join(val.split(','))            
            for key, val in filters.items():
                filter_string += f'&{key}={val}'   
  
        agrup_metric=st.selectbox('Escoja la métrica de agrupación',['Suma','Promedio','Mínimo','Máximo','Desviación estándar','Varianza', 'Conteo'],0)
        DF=st.button('Generar base de datos')   
        
        if  columnsagrupIngTvporSus_len!=0 and DF==True:
            IngTVporSus=API(id_ingresos_TVporSus,fields_str,columns_groupby_API,filter_string,Agroup_metric[agrup_metric],valagrupIngTVporSus)  
            if IngTVporSus.empty==True:
                st.warning('No se encontraron datos con los campos o filtros seleccionados. Por favor verifique la información suministrada.', icon="⚠️")
            else:
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    progress_bar.progress(i)                        
                AgGrid(IngTVporSus,width_mode='fit_columns')
                st.download_button(label="Descargar CSV",data=convert_df(IngTVporSus),file_name='Ingresos_TV_Suscripcion.csv',mime='text/csv')       

        cols_ingTVporsus=columns_dict('ingTVporsus')
        diff_cols_ingTVporsus=list(set(GetAllColumns(id_ingresos_TVporSus))^set(cols_ingTVporsus))
        if len(diff_cols_ingTVporsus)!=0:
            st.warning('Hay nombres de columnas que difieren con su diccionario.',icon="⚠️")
            st.markdown(diff_cols_ingTVporsus)
        else:    
            st.success('Toda las columnas de la base coinciden con su diccionario.')                