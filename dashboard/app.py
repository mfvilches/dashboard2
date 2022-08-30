from dash import Dash, html, dcc, Output, Input
import dash.dependencies as dd
import os
from data import resumen_semanal, resumen_semanal_geo, stop_words_sp
from graficos import get_line_comp, get_bar_top5, get_mapa, get_pie, get_wc, get_bp
import dash_bootstrap_components as dbc
from io import BytesIO
import base64

is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
if is_gunicorn:
    grupo = os.environ.get("GRUPO", "")
    requests_pathname_prefix = f"/{ grupo }"
else:
    requests_pathname_prefix = "/"

app = Dash(
    external_stylesheets=[dbc.themes.SOLAR]
)
server = app.server

app.layout = dbc.Container(
    children =[
    dbc.Row([
        dbc.Col(html.H1("Análisis de Demanda de Servicios de Urgencia en Chile"))
    ], align="center"
    ),
    dbc.Alert(
    dbc.Col(["Región:",dbc.Select(id="Region1",options=[
        {"label":"Arica y Parinacota","value":15},
        {"label":"Tarapacá","value":1},
        {"label":"Antofagasta","value":2},
        {"label":"Atacama","value":3},
        {"label":"Coquimbo","value":4},
        {"label":"Valparaiso","value":5},
        {"label":"Metropolitana","value":13},
        {"label":"O'Higgins","value":6},
        {"label":"Maule","value":7},
        {"label":"Ñuble","value":16},
        {"label":"Biobío","value":8},
        {"label":"Araucanía","value":9},
        {"label":"Ríos","value":14},
        {"label":"Lagos","value":10},
        {"label":"Aysén","value":11},
        {"label":"Magallanes","value":12},]
        , value=15)
        ],width=3), color="success"),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id="grafico1", figure=get_bar_top5(resumen_semanal,15)),],width=6),
       dbc.Col([dcc.Graph(id="grafico3", figure=get_pie(resumen_semanal,15)),],width=6),
    ], align="center"
    ),

    dbc.Row([
        dbc.Col([dcc.Graph(id="grafico2", figure= get_mapa(resumen_semanal_geo,"Código Región",15,'LATITUD      [Grados decimales]',
       'LONGITUD [Grados decimales]','total','total','nestablecimiento',6))],width=12),
    ], align="center"
    ),

    
    
    dbc.Alert(
    dbc.Col(["Establecimiento:",dbc.Select(id="Est1",options=[])
        ],width=3), color="success"),

    dbc.Row([
        dbc.Col([dcc.Graph(id="grafico4", figure=get_line_comp(resumen_semanal,15)),],width=8),
        dbc.Col(html.Img(id="image_wc"),width=4)
    ], align="center"
    ),

    dbc.Row([
        dbc.Col([dcc.Graph(id="grafico5", figure=get_bp(resumen_semanal,'Hospital Dr. Juan Noé Crevanni (Arica)')),],width=12),
    ], align="center"
    ),

    
    ],

    
    
    className="m-5"
)

@app.callback(
    Output('Est1','options'),
    Input('Region1','value')
)
def set_establecimiento(chosen_region):
    resumen_semanal_region = resumen_semanal[resumen_semanal['Código Región']==int(chosen_region)]
    return [{'label':c,'value':c} for c in sorted(resumen_semanal_region['nestablecimiento'].unique())]

@app.callback(Output("grafico1","figure"),Input("Region1","value"))
def update_grafico1(value):
    return get_bar_top5(resumen_semanal,int(value))
@app.callback(Output("grafico2","figure"),Input("Region1","value"))
def update_grafico2(value):
    return get_mapa(resumen_semanal_geo,"Código Región",int(value),'LATITUD      [Grados decimales]',
       'LONGITUD [Grados decimales]','total','total','nestablecimiento',6)
@app.callback(Output("grafico3","figure"),Input("Region1","value"))
def update_grafico3(value):
    return get_pie(resumen_semanal,int(value))
@app.callback(Output("grafico4","figure"),Input("Est1","value"))
def update_grafico4(value):
    return get_line_comp(resumen_semanal,value)

@app.callback(Output('image_wc', 'src'), Input('Est1','value'))
def make_image(b):
    img = BytesIO()
    if b is None:
        get_wc(resumen_semanal,'Hospital Dr. Juan Noé Crevanni (Arica)',stop_words_sp).save(img, format='PNG')   
    else:
        get_wc(resumen_semanal,b,stop_words_sp).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(Output("grafico5","figure"),Input("Est1","value"))
def update_grafico5(value):
    return get_bp(resumen_semanal,value)

#@app.callback(Output("grafico5","figure"),Input("Est1","value"))
#def update_grafico5(value):
#    if value is None:
#        return get_wc(resumen_semanal,"Hospital Dr. Juan Noé Crevanni (Arica)",stop_words_sp)
#    else:
#        return get_wc(resumen_semanal,value,stop_words_sp)



if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="5050")
