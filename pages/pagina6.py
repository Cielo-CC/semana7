import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/modelo-sir', name='Modelo SIR')

# Layout de la aplicación
layout = html.Div(children=[  
    html.Div(children=[
        # Contenedor izquierdo - Controles
        html.Div(children=[  
            html.H1("Modelo SIR"),
            
            html.Div([
                html.Div([
                    html.Label("Población Total (N):"),
                    dcc.Input(id="input-poblacion", type="number", value=7138, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de transmisión (β):"),
                    dcc.Input(id="input-beta", type="number", value=1.0, step=0.01, min=0.01, max=1.0, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de recuperación (γ):"),
                    dcc.Input(id="input-gamma", type="number", value=0.4, step=0.01, min=0.01, max=1.0, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Infectados iniciales (I₀):"),
                    dcc.Input(id="input-infectados", type="number", value=1, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tiempo de simulación (días):"),
                    dcc.Input(id="input-tiempo", type="number", value=40, min=10, className="input-field")
                ], className="input-group"),
                
                html.Button("Simular Epidemia", id="btn-simular", className="btn-generar")
            ], className="controls-container"),
            
            # Información de la epidemia
            html.Div(id="info-epidemia", className="info-container"),
            
            # Explicación del modelo
            html.Div([
                html.H3("Acerca del Modelo SIR:"),
                html.P("El modelo SIR divide la población en tres grupos:"),
                html.Ul([
                    html.Li("S - Susceptibles (personas sanas)"),
                    html.Li("I - Infectados (personas contagiadas)"),
                    html.Li("R - Recuperados (personas inmunes)")
                ]),
                html.P("Ecuaciones diferenciales:"),
                html.P("dS/dt = -β * S * I / N"),
                html.P("dI/dt = β * S * I / N - γ * I"),
                html.P("dR/dt = γ * I")
            ], className="info-container")
            
        ], className="left-container"),
        
        # Contenedor derecho - Gráfico
        html.Div(children=[
            html.H1("Evolución de la Epidemia"),
            html.Div([
                dcc.Graph(
                    id='grafico-sir',
                    config={'displayModeBar': True},
                    style={'height': '600px', 'width': '100%'}
                )
            ], className="graph-container")
        ], className="right-container")
    ], className="main-container")
])

# Función para simular el modelo SIR usando el método de Euler (sin scipy)
def simular_sir_euler(N, beta, gamma, I0, t_max):
    # Condiciones iniciales
    S = [N - I0]  # Susceptibles iniciales
    I = [I0]      # Infectados iniciales  
    R = [0]       # Recuperados iniciales
    
    # Vector de tiempo
    t = list(range(t_max))
    
    # Resolver usando método de Euler
    for i in range(1, t_max):
        # Calcular derivadas
        dS = -beta * S[i-1] * I[i-1] / N
        dI = beta * S[i-1] * I[i-1] / N - gamma * I[i-1]
        dR = gamma * I[i-1]
        
        # Actualizar valores
        S.append(S[i-1] + dS)
        I.append(I[i-1] + dI)
        R.append(R[i-1] + dR)
    
    return t, S, I, R

# Callback para actualizar la simulación SIR
@callback(
    [Output('grafico-sir', 'figure'),
     Output('info-epidemia', 'children')],
    Input('btn-simular', 'n_clicks'),
    [State('input-poblacion', 'value'),
     State('input-beta', 'value'),
     State('input-gamma', 'value'),
     State('input-infectados', 'value'),
     State('input-tiempo', 'value')],
    prevent_initial_call=False
)
def actualizar_simulacion_sir(n_clicks, N, beta, gamma, I0, t_max):
    # Valores por defecto si es la primera carga
    if n_clicks is None:
        N = 7138
        beta = 1
        gamma = 0.4
        I0 = 1
        t_max = 40
    
    # Validar entradas
    if I0 >= N:
        I0 = N - 1
    
    # Simular modelo SIR
    t, S, I, R = simular_sir_euler(N, beta, gamma, I0, t_max)
    
    # Calcular métricas importantes
    R0 = beta / gamma if gamma > 0 else float('inf')
    pico_infeccion = np.max(I)
    dia_pico = t[np.argmax(I)]
    total_recuperados = R[-1]
    
    # Gráfico principal SIR
    fig_sir = go.Figure()
    
    fig_sir.add_trace(go.Scatter(
        x=t, y=S,
        mode='lines',
        name='Susceptibles (S)',
        line=dict(color='blue', width=3)
    ))
    
    fig_sir.add_trace(go.Scatter(
        x=t, y=I,
        mode='lines',
        name='Infectados (I)',
        line=dict(color='red', width=3)
    ))
    
    fig_sir.add_trace(go.Scatter(
        x=t, y=R,
        mode='lines',
        name='Recuperados (R)',
        line=dict(color='green', width=3)
    ))
    
    # Añadir línea del pico de infección
    fig_sir.add_trace(go.Scatter(
        x=[dia_pico, dia_pico],
        y=[0, pico_infeccion],
        mode='lines',
        name='Pico de infección',
        line=dict(color='red', width=2, dash='dash'),
        showlegend=False
    ))
    
    fig_sir.update_layout(
        title="Evolución del Modelo SIR",
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=50, r=50, t=50, b=50),
        height=500
    )
    
    # Información de la epidemia
    info_content = [
        html.H4("Métricas de la Epidemia:"),
        html.P(f"Tasa básica de reproducción (R₀): {R0:.2f}"),
        html.P(f"Pico de infección: {pico_infeccion:.0f} personas (día {dia_pico})"),
        html.P(f"Total recuperados: {total_recuperados:.0f} personas"),
        html.P(f"Porcentaje infectado: {(total_recuperados/N)*100:.1f}%"),
        html.P("🔴 R₀ > 1: Epidemia creciente" if R0 > 1 else "🟢 R₀ ≤ 1: Epidemia controlada")
    ]
    
    return fig_sir, info_content