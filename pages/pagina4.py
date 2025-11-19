import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go

from utils.funciones import generar_grafico_logistico

dash.register_page(__name__, path='/logistico-interactivo', name='Logístico Interactivo')


# Layout inicial
layout = html.Div(children=[  
    html.Div(children=[
        # Contenedor izquierdo  
        html.Div(children=[  
            html.H2("Crecimiento Logístico Interactivo", className="title"),  
            
            html.Div([
                html.Div([
                    html.Label("Población inicial P₀:", className="input-label"),
                    dcc.Input(id="input-p0-logistico", type="number", value=100, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de crecimiento (r):", className="input-label"),
                    dcc.Input(id="input-r-logistico", type="number", value=0.1, step=0.01, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Capacidad de carga (K):", className="input-label"),
                    dcc.Input(id="input-k-logistico", type="number", value=1000, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tiempo máximo (t):", className="input-label"),
                    dcc.Input(id="input-t-max-logistico", type="number", value=100, min=10, className="input-field")
                ], className="input-group"),
                
                html.Button("Generar gráfica", id="btn-generar-logistico", className="btn-generar")
            ], className="controls-container")
            
        ], className="left-container"),
        
        # Contenedor derecho  
        html.Div(children=[
            html.H2("Gráfica del Modelo Logistico", className="title"),
            html.Div([
                dcc.Graph(
                    id='grafico-logistico-interactivo',
                    config={'displayModeBar': True},
                    style={'height': '500px', 'width': '100%'}
                )
            ], className="graph-container"),
        ], className="right-container")
    ], className="main-container")
])

# Callback para actualizar la gráfica logística
@callback(
    Output('grafico-logistico-interactivo', 'figure'),
    Input('btn-generar-logistico', 'n_clicks'),
    [State('input-p0-logistico', 'value'),
     State('input-r-logistico', 'value'),
     State('input-k-logistico', 'value'),
     State('input-t-max-logistico', 'value')],
    prevent_initial_call=False
)
def actualizar_grafica_logistica(n_clicks, P0, r, K, t_max):
    fig = generar_grafico_logistico(P0, r, K, t_max)
    return fig