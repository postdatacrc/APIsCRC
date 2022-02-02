import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import glob
import os
from urllib.request import urlopen
import json
import io
import requests
from streamlit_folium import folium_static
from st_aggrid import AgGrid
import geopandas as gpd
import folium

LogoComision="data:image/png;base64,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"
LogoComision2="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

st.set_page_config(
    page_title="Similitud e indicador exactitud", page_icon=LogoComision,layout="wide",initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True)       
st.markdown("""<style type="text/css">
    h1{ background: #FA7268;
    text-align: center;
    padding: 15px;
    font-family: sans-serif;
    font-size:1.60rem;
    color: black;
    position:fixed;
    width:100%;
    z-index:9999;
    top:80px;
    left:0;}
    .css-m70y {display:none}
    .barra-superior{top: 0;
    position: fixed;
    background-color: #2e297b;
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
    .main, .css-1lcbmhc > div{margin-top:135px;}
    .css-y3whyl, .css-xqnn38 {background-color:#ccc}
    .css-1uvyptr:hover,.css-1uvyptr {background: #ccc}
    .block-container {padding-top:0;}
    h2{
    background: #fffdf7;
    text-align: center;
    background-color:#f0e9e9;
    padding: 10px;
    text-decoration: underline;
    text-decoration-style: double;
    color: #27348b;}
    h3{ border-bottom: 2px solid #2e297b;
    border-left: 10px solid #2e297b;
    background: #f0e9e9;
    padding: 10px;
    color: black;}
    h4{
    color: #2e297b;}
    .imagen-flotar{float:left;}
    @media (max-width:1230px){
        .barra-superior{height:160px;} 
        .main, .css-1lcbmhc > div{margin-top:215px;}
        .imagen-flotar{float:none}
        h1{top:160px;}
    }    
    </style>""", unsafe_allow_html=True)  
st.markdown("""
<div class="barra-superior">
    <div class="imagen-flotar" style="height: 70px; left: 10px; padding:15px">
        <a class="imagen-flotar" style="float:left;" href="https://www.crcom.gov.co" title="CRC">
            <img src="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png" alt="CRC" style="height:40px">
        </a>
        <a class="imagen-flotar" style="padding-left:10px;" href="https://www.postdata.gov.co" title="Postdata">
            <img src="https://www.postdata.gov.co/sites/default/files/postdata-logo.png" alt="Inicio" style="height:40px">
        </a>       
    </div>
</div>""",unsafe_allow_html=True)    

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except:
        print("El formato de fecha es incorrecto, debería ser dd-mm-aa")

st.title("Similitud entre base-diccionario y calculador indicador exactitud")

na_values = ["", 
             "#N/A", 
             "#N/A N/A", 
             "#NA", 
             "-1.#IND", 
             "-1.#QNAN", 
             "-NaN", 
             "-nan", 
             "1.#IND", 
             "1.#QNAN", 
             "<NA>", 
             "N/A", 
#              "NA", 
             "NULL", 
             "NaN", 
             "n/a", 
             "nan", 
             "null"]
col1a, col2a = st.columns(2)
with col1a:
    st.write("### Base de datos")
    dataset = st.file_uploader("Suba o arrastre la base", type = ['csv'])

    if dataset is not None:
        if dataset.name.startswith('DICC')==True:
            st.write('Por favor cargue aquí la base de datos, no el diccionario')
        else:    
            dataset.seek(0)
            colsbase=[];
            BASE = pd.read_csv(dataset,delimiter=';',keep_default_na=False,na_values=na_values,encoding='latin-1',low_memory=False)
            colsbase=BASE.columns.tolist()
            colsbase=[elem.replace("ï»¿", "") for elem in colsbase]
            BASE.columns=colsbase
            AgGrid(BASE.tail(100))

with col2a:
    st.write("### Diccionario")
    dicset = st.file_uploader("Suba o arrastre el diccionario", type = ['csv'])
    
    if dicset is not None:
        if dicset.name.startswith('DICC')==False:
            st.write('Por favor cargue aquí el diccionario, no la base de datos')
        else:    
            dicset.seek(0)
            DIC = pd.read_csv(dicset,delimiter=';',keep_default_na=False,na_values='NA',encoding='latin-1',low_memory=False)
            AgGrid(DIC)
                    
if dataset is not None and dicset is not None:
    st.write("### Similitud entre la base y su diccionario")
    st.write("""<ul><li><h4>Coincidencia nombres</h4></li></ul>""",unsafe_allow_html=True)
    if len(BASE.columns.to_list())==len(DIC['CAMPO'].unique()):
        st.write("##### Primero se verificará que los nombres de las columnas de la base coincidan con su diccionario")
        st.write("¿Los nombres del diccionario coinciden con las columnas de la base?",sorted(BASE.columns.to_list()) == sorted(DIC['CAMPO'].unique()))   
        if len(list(set(BASE.columns)^(set(DIC['CAMPO'].unique()))))==0:
            st.write('¡Muy bien! no hay columnas que difieran entre la base y el diccionario')
        else:
            st.warning('Hay discrepancias en los nombres de las bases y el diccionario. Las columnas que difieren son:')
            st.warning(list(sorted(set(BASE.columns)^(set(DIC['CAMPO'].unique())))))
            set(BASE.columns).symmetric_difference(set(DIC['CAMPO'].unique()))
            BASE.columns=DIC['CAMPO'].unique()
    else:   
        st.warning("El número de columnas de la base no coincide con los campos del diccionario. Para proceder corrija la base y/o diccionario")
        
    st.write("""<ul><li><h4>Coincidencia tipo de dato</h4></li></ul>""",unsafe_allow_html=True)       
    st.write("##### En primer lugar se verifica que los tipos de datos reportados en el diccionario sean los correctos.")     
    tipo_de_dato={'Numérico':['int64','float','float64','int'],'Texto':['str','O'],'Fecha':['str','O'],'Hora':['str','O']}
    td_aprobado=['Numérico','Texto','Fecha','Hora']
    columnas=DIC['CAMPO'].unique().tolist()    
    nombresDic=DIC.columns.values.tolist()
    nombresDic=[elem.lower() for elem in nombresDic]
    coincidenciadato=[]
    tipodato=[]
    if 'tipo de dato' not in nombresDic:
        st.warning('La columna que tiene la información sobre la categoría del dato se debe llamar "TIPO DE DATO". Se debe corregir el diccionario')
    else:
        tipo_dato_en_dic=DIC['TIPO DE DATO'].unique().tolist()
        diftipodato=list(set(tipo_dato_en_dic)-set(td_aprobado))
        if len(diftipodato) >0:
            st.write("""<b>ERROR!!</b>""",unsafe_allow_html=True)
            st.warning('Hay tipos de dato en el diccionario que no concuerdan con los valores permitidos: [Texto,Numérico,Fecha,Hora]')
            st.write('Los valores que están en el diccionario y no están permitidos son')
            st.warning(diftipodato)
        else: 
            st.write("""<b>Muy bien!!</b> los tipos de datos reportados en el diccionario son correctos!""",unsafe_allow_html=True)
            colsNum=DIC[DIC['TIPO DE DATO']=='Numérico']['CAMPO'].unique().tolist()
            BASENUM=BASE[colsNum]
            BASENUM=BASENUM.select_dtypes(include=['O'])
            BASENUM=BASENUM.apply(lambda x: x.str.replace(',','.'))
            colsBASENUM=BASENUM.columns.values.tolist()
            BASENUM2=BASENUM.copy()
            BASENUM2[colsBASENUM] = BASENUM2[colsBASENUM].apply(pd.to_numeric, errors='coerce')            
            colsthatcanchange=BASENUM2.isna().sum()[BASENUM2.isna().sum() == 0].index.tolist()
            BASE[colsthatcanchange]=BASE[colsthatcanchange].apply(lambda x: x.str.replace(',','.'))
            BASE[colsthatcanchange] = BASE[colsthatcanchange].apply(pd.to_numeric, errors='coerce')  

            for elem in columnas:
                coincidenciadato.append(BASE[elem].dtypes in tipo_de_dato[DIC[DIC['CAMPO']==elem]['TIPO DE DATO'].values.tolist()[0]])
                tipodato.append(DIC[DIC['CAMPO']==elem]['TIPO DE DATO'].values.tolist()[0])
            st.write("##### Ahora se verificará la coincidencia entre el tipo de dato de cada columna de la base y lo reportado en su diccionario")                           
            dictcoincidence={'Columnas':columnas,'Tipo de dato':tipodato,'Coincidencia':coincidenciadato}
            dfcoincidencia=pd.DataFrame.from_dict(dictcoincidence) 
            st.write(dfcoincidencia)
            if False in dfcoincidencia.Coincidencia.unique().tolist():
                st.warning('las siguientes columnas no tienen el tipo de dato correcto y deben ser corregidas:')
                st.write(dfcoincidencia[dfcoincidencia['Coincidencia']==False]['Columnas'].values.tolist())    
        # if 'FECHA' in columnas:
            # st.write("""<ul><li><h4>Verificaciones adicionales</h4></li></ul>""",unsafe_allow_html=True)
            # st.write('True')
            # st.write(BASE['FECHA'])
            # fechas=BASE['FECHA'].values.tolist()
            # errorFechas=list(map(validate,fechas))
            # if len(errorFechas)==BASE.shape[0]:
                # st.write('Toda la columna tiene el formato incorrecto')
            # else:
                # st.write("Hay",len(errorFechas),"con error en su formato")
            
            
            
###################################################################################################################################################

if dataset is not None:
    if dataset.name.startswith('DICC')==False:
        st.write("### Calculador completitud")
        st.write("#### Dimensión de la base")
        NFXC=BASE.shape[0]*BASE.shape[1] #Número de filas por columnas
        st.write('El número de filas por columnas es:',NFXC)
        st.write("#### Espacios vacíos en la base")
        Espaciosvacios=[str(len(BASE[BASE[cols] == ''])) for cols in BASE.columns]
        Columnas=BASE.columns.values
        ColsEspaciosvacios=[a+'='+b for a,b in zip(Columnas,Espaciosvacios)]
        NEV=sum([len(BASE[BASE[cols] == '']) for cols in BASE.columns]) #Número de espacios vacíos en la base de datos
        st.write('los números de los espacios vacíos en las columnas son:')
        st.write(ColsEspaciosvacios)
        st.write("#### Espacios nulos en la base")
        Columnasfloat=BASE.loc[:, BASE.dtypes == np.float64].columns.tolist()
        Columnasint=BASE.loc[:, BASE.dtypes == np.int64].columns.tolist()
        Columnasstr=BASE.loc[:, BASE.dtypes == object].columns.tolist()
        NAfloats=sum([BASE[cols].isnull().values.sum() for cols in Columnasfloat]) #Número de campos nulos en columnas numéricas tipo float
        NAint=sum([BASE[cols].isnull().values.sum() for cols in Columnasint]) #Número de campos nulos en columnas numéricas tipo int
        Ntot=NAfloats+NAint
        ColsintNA=[a+'='+b for a,b in zip(Columnasint,[str(BASE[cols].isnull().values.sum()) for cols in Columnasint])]
        ColsfloatNA=[a+'='+b for a,b in zip(Columnasfloat,[str(BASE[cols].isnull().values.sum()) for cols in Columnasfloat])]
        ColsstrNA=[a+'='+b for a,b in zip(Columnasstr,[str(BASE[cols].isnull().values.sum()) for cols in Columnasstr])]
        st.write('Los valores nulos en las columnas son:')
        st.write(ColsintNA+ColsfloatNA+ColsstrNA)
        st.write("#### Indicador exactitud y completitud")
        IndicadorExactitud=round(2.5*(2*NFXC-Ntot-NEV)/NFXC,3)
        st.write("! El indicador de exactitud y completitud de la base es:",IndicadorExactitud,'¡')
    else:
        pass
