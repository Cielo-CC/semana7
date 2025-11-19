import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/logistico', name='Logístico')

def crear_grafico_logistico():
    P0 = 100      
    r = 0.1       
    K = 1000      
    t = np.linspace(0, 100, 200)  
    
    P = (K * P0 * np.exp(r * t)) / (K + P0 * (np.exp(r * t) - 1))
    
    trace_logistico = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        line=dict(
            color='#e74c3c',
            width=3
        ),
        marker=dict(
            color='#c0392b',
            symbol='circle',
            size=5,
            line=dict(color='white', width=1)
        ),
        hovertemplate='<b>Tiempo:</b> %{x:.1f}<br><b>Población:</b> %{y:.0f}<extra></extra>'
    )
    
    trace_capacidad = go.Scatter(
        x=[min(t), max(t)],
        y=[K, K],
        mode='lines',
        line=dict(
            color='#2ecc71',
            width=2,
            dash='dot'
        ),
        hovertemplate='<b>Capacidad de Carga:</b> %{y:.0f}<extra></extra>'
    )
    
    fig = go.Figure(data=[trace_logistico, trace_capacidad])
    
    fig.update_layout(
        title=dict(
            text='<b>Crecimiento Logístico de la Población</b>',
            font=dict(size=18, color='#2c3e50', family='Outfit'),
            x=0.5,
            y=0.95
        ),
        xaxis_title='<b>Tiempo (t)</b>',
        yaxis_title='<b>Población P(t)</b>',
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        font=dict(family='Outfit', size=12, color='#34495e'),
        height=450,
        showlegend=False
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#e1e8ed',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='#bdc3c7',
        showline=True, 
        linecolor='#34495e', 
        linewidth=2
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#e1e8ed',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='#bdc3c7',
        showline=True, 
        linecolor='#34495e', 
        linewidth=2
    )
    
    return fig

fig_logistico = crear_grafico_logistico()

layout = html.Div(children=[  
    html.Div(children=[
        # Contenedor izquierdo  
        html.Div(children=[  
            html.H2("Crecimiento Logístico de la Población", className="title"),  
            dcc.Markdown(r"""
El crecimiento exponencial no es una situación muy sostenible, ya que depende de cantidades infinitas de recursos (las cuales no suelen existir en el mundo real).
El crecimiento exponencial puede ocurrir durante un tiempo, si hay pocos individuos y muchos recursos, pero cuando el número de individuos es lo suficientemente grande, los recursos empiezan a agotarse, lo que desacelera la tasa de crecimiento. Finalmente, el tamaño de la población se nivelará, o se estabilizará, lo que produce una gráfica con forma de $S$. El tamaño de la población en el que el crecimiento poblacional se nivela representa el tamaño poblacional máximo que puede soportar un medio ambiente en particular y se conoce como capacidad de carga o 
$K$

** Parámetros del Modelo **

- **$P$** = Población actual
- **$t$** = Tiempo
- **$r$** = Tasa de crecimiento intrínseco
- **$K$** = Capacidad de carga (población máxima que el ambiente puede sostener)
- **$P_0$** = Población inicial

En este ejemplo:
- **$P_0 = 100$**
- **$r = 0.1$**
- **$K = 1000$**
            """, className="content", mathjax=True),
        ], className="left-container"),
        
        html.Div(children=[
            html.H2("Grafica", className="title"),
            html.Div([
                dcc.Graph(
                    id='grafico-logistico',
                    figure=fig_logistico,
                    config={'displayModeBar': False},
                    style={'height': '450px', 'width': '100%'}
                )
            ], className="graph-container"),
        ], className="right-container")
    ], className="main-container")
])