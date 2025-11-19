import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go
import math

dash.register_page(__name__, path='/campo-vectorial', name='Campo Vectorial')

# Layout de la aplicación
layout = html.Div(children=[  
    html.Div(children=[
        # Contenedor izquierdo - Controles
        html.Div(children=[  
            html.H1("Campo Vectorial"),
            
            html.Div([
                html.Div([
                    html.Label("Ecuación dx/dt =", className="input-label"),
                    dcc.Input(id="input-fx", type="text", value="X", className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Ecuación dy/dt =", className="input-label"),
                    dcc.Input(id="input-fy", type="text", value="Y", className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Rango del Eje X:", className="input-label"),
                    dcc.Input(id="input-xmax", type="number", value=5, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Rango del Eje Y:", className="input-label"),
                    dcc.Input(id="input-ymax", type="number", value=5, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Mallado:", className="input-label"),
                    dcc.Input(id="input-n", type="number", value=20, min=5, max=50, className="input-field")
                ], className="input-group"),
                
                html.Button("Generar Campo Vectorial", id="btn-generar", className="btn-generar")
            ], className="controls-container"),
            
            # Información del campo vectorial
            html.Div(id="info-campo", className="info-container"),
            
            # Ejemplos para probar
            html.Div([
                html.H3("Ejemplos para probar:"),
                html.Ul([
                    html.Li("dx/dt = X, dy/dt = Y"),
                    html.Li("dx/dt = -Y, dy/dt = X"),
                    html.Li("dx/dt = X + Y, dy/dt = np.cos(Y)"),
                    html.Li("dx/dt = np.sin(Y), dy/dt = np.cos(X)")
                ], className="examples-list")
            ], className="examples-container")
            
        ], className="left-container"),
        
        # Contenedor derecho - Gráfico
        html.Div(children=[
            html.H1("Visualización del Campo Vectorial"),
            html.Div([
                dcc.Graph(
                    id='grafico-campo-vectorial',
                    config={'displayModeBar': True},
                    style={'height': '700px', 'width': '100%'}
                )
            ], className="graph-container"),
        ], className="right-container")
    ], className="main-container")
])

# Función para generar el campo vectorial
def generar_campo_vectorial(fx_str, fy_str, xmax, ymax, n):
    # Crear la malla
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    
    # Evaluar las funciones dx/dt y dy/dt
    try:
        # Preparar el contexto para eval
        context = {
            'np': np,
            'math': math,
            'X': X,
            'Y': Y,
            'sin': np.sin,
            'cos': np.cos,
            'exp': np.exp,
            'log': np.log,
            'sqrt': np.sqrt
        }
        
        # Evaluar U (dx/dt) y V (dy/dt)
        U = eval(fx_str, context)
        V = eval(fy_str, context)
        
        # Calcular magnitud
        magnitude = np.sqrt(U**2 + V**2)
        
        return X, Y, U, V, magnitude
    
    except Exception as e:
        print(f"Error al evaluar las funciones: {e}")
        # Retornar campo cero en caso de error
        return X, Y, np.zeros_like(X), np.zeros_like(Y), np.zeros_like(X)

# SOLUCIÓN: Un solo callback que maneje tanto la inicialización como las actualizaciones
@callback(
    [Output('grafico-campo-vectorial', 'figure'),
     Output('info-campo', 'children')],
    Input('btn-generar', 'n_clicks'),
    [State('input-fx', 'value'),
     State('input-fy', 'value'),
     State('input-xmax', 'value'),
     State('input-ymax', 'value'),
     State('input-n', 'value')],
    prevent_initial_call=False  # Permitir llamada inicial
)
def actualizar_campo_vectorial(n_clicks, fx, fy, xmax, ymax, n):
    # Si es la primera carga (n_clicks es None), usar valores por defecto
    if n_clicks is None:
        fx = "np.sin(Y)"
        fy = "np.cos(X)"
        xmax = 5
        ymax = 5
        n = 15
    
    if n is None or n < 5:
        n = 15
    
    X, Y, U, V, magnitude = generar_campo_vectorial(fx, fy, xmax, ymax, n)
    
    # Crear la figura para campo vectorial 2D
    fig = go.Figure()
    
    # Normalizar vectores para mejor visualización
    max_magnitude = np.max(magnitude)
    if max_magnitude > 0:
        U_norm = U / max_magnitude
        V_norm = V / max_magnitude
    else:
        U_norm = U
        V_norm = V
    
    # Crear flechas para el campo vectorial
    arrow_scale = 0.8 * min(xmax, ymax) / n  # Escala automática
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if magnitude[i, j] > 0:  # Solo dibujar flechas donde hay magnitud
                x_start = X[i, j]
                y_start = Y[i, j]
                x_end = x_start + U_norm[i, j] * arrow_scale
                y_end = y_start + V_norm[i, j] * arrow_scale
                
                # Añadir flecha
                fig.add_trace(go.Scatter(
                    x=[x_start, x_end],
                    y=[y_start, y_end],
                    mode='lines+markers',
                    line=dict(
                        color='blue',
                        width=2
                    ),
                    marker=dict(
                        symbol='arrow',
                        size=10,
                        angleref='previous',
                        color='red'
                    ),
                    showlegend=False
                ))
    
    # Configurar el layout
    fig.update_layout(
        title=f"Campo Vectorial: dx/dt = {fx}, dy/dt = {fy}",
        xaxis_title='X',
        yaxis_title='Y',
        xaxis=dict(range=[-xmax, xmax], constrain='domain'),
        yaxis=dict(range=[-ymax, ymax], scaleanchor="x", scaleratio=1),
        margin=dict(l=0, r=0, t=50, b=0),
        height=650,
        showlegend=False
    )
    
    # Crear información del campo
    magnitud_min = np.min(magnitude)
    magnitud_max = np.max(magnitude)
    
    info_content = [
        html.H4("Información del Campo Vectorial"),
        html.P(f"Ecuaciones: dx/dt = {fx}, dy/dt = {fy}"),
        html.P(f"Magnitud: min = {magnitud_min:.2f}, max = {magnitud_max:.2f}"),
        html.P(f"Rango X: [-{xmax}, {xmax}], Rango Y: [-{ymax}, {ymax}]"),
        html.P(f"Mallado: {n} x {n} puntos")
    ]
    
    return fig, info_content