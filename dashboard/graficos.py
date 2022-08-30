import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_line(data,id,gc):
    data_id = data[(data.idestablecimiento == id)&(data.glosacausa == gc)]
    fig = px.line(data_id,x='semana',y='total',markers=True)
    return fig

def get_line_edad(data,id,gc,edad):
    data_id = data[(data.idestablecimiento == id)&(data.glosacausa == gc)]
    fig = px.line(data_id,x='semana',y=edad,markers=True,
    labels={
                     "value": "# de Pacientes",
                     "variable": "Edades",
                     "semana":"Semanas"
            }
        )
    fig.update_layout(font_family="Courier New",title_font_family="Courier New")
    return fig


def get_line_comp(data,id):
    data_id = data[(data.nestablecimiento == id)]
    fig = px.line(data_id,x='semana',y='total',markers=True,color = 'glosacausa', template="plotly_dark",
    labels={
                     "glosacausa": "Patologías",
                     "total":"# de Atenciones Semanales",
                     "semana":"Semana del Año"

            }
        ,title = "Evolución temporal de Demanda por patología")
    return fig

def get_bar(data):
    fig = px.bar(data, x=data.idestablecimiento,y=['Menor a 1 año','De 1 a 4 años','De 5 a 14 años','De 15 a 64 años','65 años y más'], template="plotly_dark"
    ,labels={
                     "value": "# de Pacientes",
                     "variable": "Edades",
                     "nestablecimiento":""

            }
    )
    return fig

def get_mapa(data,columna,filtro,lat,lon,color,size,hover,zoom):
    px.set_mapbox_access_token('pk.eyJ1IjoibXZpbGNoZXNwIiwiYSI6ImNsNzI3Y2NnbjB2a2Qzb212YzFuNDUzbmEifQ.3HfsObdHujRthrYnDCBZUw')
    fig = px.scatter_mapbox(data[(data[columna] == filtro)], lat=lat, lon=lon, color=color, size=size, size_max=18, zoom=zoom, hover_name=hover, template= 'plotly_dark')
    return fig

def get_bar_top5(data,region):
    data_id = data[data['Código Región']==region]
    data_id = data_id.groupby(by=['idestablecimiento','nestablecimiento'],as_index=False).sum().sort_values(by='total',ascending=False)[:5]
    fig = px.bar(data_id, x=data_id.nestablecimiento,y=['Menor a 1 año','De 1 a 4 años','De 5 a 14 años','De 15 a 64 años','65 años y más'], template= 'plotly_dark',
    labels={
                     "value": "# de Pacientes",
                     "variable": "Edades",
                     "nestablecimiento":"Centro"

            },title = "Top 5 Centros con más atenciones")
    fig.update_layout(showlegend=False)
    
    return fig

def get_pie(data,region):
    data_id = data[data['Código Región']==region]
    data_id = data_id.groupby(by=['Código Región'],as_index=False).sum().sort_values(by='total',ascending=False)
    data_id.drop(columns=['semana','Idcausa','total'],inplace=True)
    data_long = data_id.melt(id_vars='Código Región',value_name='count')
    fig = px.pie(data_long, values='count', names=['Menor a 1 año','De 1 a 4 años','De 5 a 14 años','De 15 a 64 años','65 años y más'], hole =.3, template='plotly_dark',
    labels={
                     "value": "# de Pacientes",
                     "count": "Tramo Etario",
                     "label":"Tramo Etario"

            },title = "Demanda por Tramo Etario")
    fig.update_traces(sort=False) 
    return fig

def get_wc(data,id,stopwords):
    data_id = data[(data.nestablecimiento == id)]
    text = " ".join(review for review in data_id['glosacausa'].astype(str))
    meta_wc = WordCloud(
    background_color='black',
    width=370, 
    height=450,
    max_words=300,
    stopwords=stopwords
    )
    # generamos la word cloud
    meta_wc.generate(text)
    return meta_wc.to_image()

def get_bp (data,id):
    data_id = data[(data.nestablecimiento == id)]
    data_id = data_id.groupby(by=['semana'],as_index=False).sum()
    fig = px.box(data_id, y="total", template='plotly_dark', points="all",
    labels={
                     "value": "# de Pacientes semanales",
                     "total":"# de Atenciones Semanales"

            }
        ,title = "Distribución de Demanda Semanal")
    return fig




