import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
from utils.funciones import generar_graf_pob_exp

dash.register_page(__name__, path='/exponencial-interactivo', name='Exponencial Interactivo')

# Layout inicial con valores por defecto
layout = html.Div(children=[  
    html.Div(children=[  
            # Controles de entrada
html.H2("Crecimiento Exponencial de la Población", className="title"), 
            html.Div([
                html.Div([
                    html.Label("Población inicial P(0):", className="input-label"),
                    dcc.Input(id="input-p0", type="number", value=100, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de crecimiento (r):", className="input-label"),
                    dcc.Input(id="input-r", type="number", value=0.03, step=0.01, min=0.01, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tiempo máximo (t):", className="input-label"),
                    dcc.Input(id="input-t", type="number", value=100, min=10, className="input-field")
                ], className="input-group"),
                
                html.Button("Generar gráfica", id="btn-generar", className="btn-generar")
            ], className="controls-container")
        ], className="left-container"),
        
        # Contenedor derecho  
        html.Div(children=[
            html.H2("Gráfica del Modelo Exponencial", className="title"),
            html.Div([
                dcc.Graph(
                    id='grafico-crecimiento',
                    config={'displayModeBar': False},
                    style={'height': '500px', 'width': '100%'}
                )
            ], className="graph-container")
        ], className="right-container")
    ], className="main-container")


# Callback para actualizar la gráfica
@callback(
    Output('grafico-crecimiento', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, t_max):
    fig = generar_graf_pob_exp(P0, r, t_max)
    return fig