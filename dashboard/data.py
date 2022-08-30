import pandas as pd
import nltk
from nltk.corpus import stopwords
data_url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/gapminderData.csv"
gapminder = pd.read_csv(data_url)

df = pd.read_csv('AtencionesUrgencia.csv')
df = df[~df.glosacausa.isin(['\xa0- LAS DEMÁS CAUSAS',
       'Pacientes en espera de hospitalización que esperan menos de 12 horas para ser trasladados a cama hospitalaria',
       'CAUSAS SISTEMA RESPIRATORIO',
       '\xa0- TRAUMATISMOS Y ENVENENAMIENTOS',
       'SECCIÓN 2. TOTAL DE HOSPITALIZACIONES', 'CIRUGÍAS DE URGENCIA', 'Pacientes en espera de hospitalización','\xa0-\xa0CAUSAS SISTEMA CIRCULATORIO'])]
df2 = df[~((df.semana == 1) & ((df.fecha == '30/12/2018') | (df.fecha == '31/12/2018')))]
df2 = df2.reset_index()
df_g = df2[~df2.glosacausa.isin(['TOTAL CAUSAS SISTEMA CIRCULATORIO','TOTAL DEMÁS CAUSAS', 'TOTAL CAUSAS SISTEMA RESPIRATORIO','SECCIÓN 1. TOTAL ATENCIONES DE URGENCIA','TOTAL TRAUMATISMOS Y ENVENENAMIENTO'])]
df_t = df2[df2.glosacausa.isin(['TOTAL CAUSAS SISTEMA CIRCULATORIO','TOTAL DEMÁS CAUSAS', 'TOTAL CAUSAS SISTEMA RESPIRATORIO','SECCIÓN 1. TOTAL ATENCIONES DE URGENCIA','TOTAL TRAUMATISMOS Y ENVENENAMIENTO'])]       
es = pd.read_excel('est_pais.xlsx')
es.drop(columns=['Fecha de Incorporación a la base o cambios',
       'Unnamed: 29', 'Unnamed: 30', 'Unnamed: 31'],inplace=True)
df3 = (
    df_g.merge(es, 
              left_on=['idestablecimiento'],
              right_on=['Código Antiguo '],
              how='left', 
              indicator=True)
    .query('_merge == "both"')
    .drop(columns='_merge')
)
df3=df3.drop(columns=['index'])
df3.rename(columns = {'Col01':'total', 'Col02':'Menor a 1 año','Col03':'De 1 a 4 años','Col04':'De 5 a 14 años','Col05':'De 15 a 64 años','Col06':'65 años y más'}, inplace = True)
resumen_semanal=df3.groupby(by=['semana','idestablecimiento','glosacausa','Código Región','nestablecimiento'],as_index=False).sum()
resumen_semanal_geo=df3.groupby(by=['nestablecimiento','idestablecimiento','LATITUD      [Grados decimales]','LONGITUD [Grados decimales]','Código Región'],as_index=False).sum()
nltk.download('stopwords')
stop_words_sp = set(stopwords.words('spanish'))