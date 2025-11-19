import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/modelo-seir', name='Modelo SEIR', suppress_callback_exceptions=True)

layout = html.Div(children=[  
    html.Div(children=[
        html.Div(children=[  
            html.H1("Modelo SEIR"),
            
            html.Div([
                html.Div([
                    html.Label("Población Total (N):"),
                    dcc.Input(id="input-poblacion", type="number", value=1000, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de transmisión (β):"),
                    dcc.Input(id="input-beta", type="number", value=0.5, step=0.01, min=0.01, max=1.0, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de incubación (σ):"),
                    dcc.Input(id="input-sigma", type="number", value=0.2, step=0.01, min=0.01, max=1.0, className="input-field"),
                    html.Small("1/σ = período de incubación (días)", style={"color": "gray"})
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tasa de recuperación (γ):"),
                    dcc.Input(id="input-gamma", type="number", value=0.1, step=0.01, min=0.01, max=1.0, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Expuestos iniciales (E₀):"),
                    dcc.Input(id="input-expuestos", type="number", value=1, min=1, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Infectados iniciales (I₀):"),
                    dcc.Input(id="input-infectados", type="number", value=0, min=0, className="input-field")
                ], className="input-group"),
                
                html.Div([
                    html.Label("Tiempo de simulación (días):"),
                    dcc.Input(id="input-tiempo", type="number", value=150, min=10, className="input-field")
                ], className="input-group"),
                
                html.Button("Simular Epidemia", id="btn-simular", className="btn-generar")
            ], className="controls-container"),
            
            html.Div(id="info-epidemia-seir", className="info-container"),
            
        ], className="left-container"),
        
        html.Div(children=[
            html.H1("Evolución de la Epidemia"),
            html.Div([
                dcc.Graph(
                    id='grafico-seir',
                    config={'displayModeBar': True},
                    style={'height': '600px', 'width': '100%'}
                )
            ], className="graph-container")
        ], className="right-container")
    ], className="main-container")
])

def simular_seir_euler(N, beta, sigma, gamma, E0, I0, t_max):
    S = [N - E0 - I0]  # Susceptibles iniciales
    E = [E0]           # Expuestos iniciales
    I = [I0]           # Infectados iniciales  
    R = [0]            # Recuperados iniciales
    
    t = list(range(t_max))
    
    for i in range(1, t_max):
        dS = -beta * S[i-1] * I[i-1] / N
        dE = beta * S[i-1] * I[i-1] / N - sigma * E[i-1]
        dI = sigma * E[i-1] - gamma * I[i-1]
        dR = gamma * I[i-1]
        
        S.append(S[i-1] + dS)
        E.append(E[i-1] + dE)
        I.append(I[i-1] + dI)
        R.append(R[i-1] + dR)
        
        S[i] = max(0, S[i])
        E[i] = max(0, E[i])
        I[i] = max(0, I[i])
        R[i] = max(0, R[i])
    
    return t, S, E, I, R

@callback(
    [Output('grafico-seir', 'figure'),
     Output('info-epidemia-seir', 'children')],
    [Input('btn-simular', 'n_clicks'),
     Input('input-poblacion', 'value'),
     Input('input-beta', 'value'),
     Input('input-sigma', 'value'),
     Input('input-gamma', 'value'),
     Input('input-expuestos', 'value'),
     Input('input-infectados', 'value'),
     Input('input-tiempo', 'value')],
    prevent_initial_call=False
)
def actualizar_simulacion_seir(n_clicks, N, beta, sigma, gamma, E0, I0, t_max):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else ''
    
    if n_clicks is None and trigger_id == '':
        N = 1000
        beta = 0.5
        sigma = 0.2
        gamma = 0.1
        E0 = 1
        I0 = 0
        t_max = 150
    elif trigger_id != 'btn-simular' and n_clicks is None:
        return go.Figure(), html.Div("Actualiza los parámetros y haz clic en 'Simular Epidemia'")
    
    if N is None or N <= 0: N = 1000
    if beta is None or beta <= 0: beta = 0.5
    if sigma is None or sigma <= 0: sigma = 0.2
    if gamma is None or gamma <= 0: gamma = 0.1
    if E0 is None or E0 < 0: E0 = 1
    if I0 is None or I0 < 0: I0 = 0
    if t_max is None or t_max < 10: t_max = 150
    
    if E0 + I0 >= N:
        E0 = min(E0, N - 1)
        I0 = 0
    
    try:
        t, S, E, I, R = simular_seir_euler(N, beta, sigma, gamma, E0, I0, t_max)
        
        R0 = beta / gamma if gamma > 0 else float('inf')
        pico_infeccion = np.max(I)
        dia_pico = t[np.argmax(I)]
        pico_expuestos = np.max(E)
        dia_pico_expuestos = t[np.argmax(E)]
        total_recuperados = R[-1]
        periodo_incubacion = 1 / sigma if sigma > 0 else float('inf')
        
        fig_seir = go.Figure()
        
        fig_seir.add_trace(go.Scatter(
            x=t, y=S,
            mode='lines',
            name='Susceptibles (S)',
            line=dict(color='blue', width=3)
        ))
        
        fig_seir.add_trace(go.Scatter(
            x=t, y=E,
            mode='lines',
            name='Expuestos (E)',
            line=dict(color='orange', width=3)
        ))
        
        fig_seir.add_trace(go.Scatter(
            x=t, y=I,
            mode='lines',
            name='Infectados (I)',
            line=dict(color='red', width=3)
        ))
        
        fig_seir.add_trace(go.Scatter(
            x=t, y=R,
            mode='lines',
            name='Recuperados (R)',
            line=dict(color='green', width=3)
        ))
        
        fig_seir.add_trace(go.Scatter(
            x=[dia_pico, dia_pico],
            y=[0, pico_infeccion],
            mode='lines',
            name='Pico de infección',
            line=dict(color='red', width=2, dash='dash'),
            showlegend=False
        ))
        
        fig_seir.add_trace(go.Scatter(
            x=[dia_pico_expuestos, dia_pico_expuestos],
            y=[0, pico_expuestos],
            mode='lines',
            name='Pico de expuestos',
            line=dict(color='orange', width=2, dash='dash'),
            showlegend=False
        ))
        
        fig_seir.update_layout(
            title="Evolución del Modelo SEIR",
            xaxis_title="Tiempo (días)",
            yaxis_title="Número de personas",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=50, r=50, t=50, b=50),
            height=500
        )
        
        info_content = [
            html.H4("Métricas de la Epidemia:"),
            html.P(f"Tasa básica de reproducción (R₀): {R0:.2f}"),
            html.P(f"Período de incubación: {periodo_incubacion:.1f} días"),
            html.P(f"Pico de expuestos: {pico_expuestos:.0f} personas (día {dia_pico_expuestos})"),
            html.P(f"Pico de infección: {pico_infeccion:.0f} personas (día {dia_pico})"),
            html.P(f"Total recuperados: {total_recuperados:.0f} personas"),
            html.P(f"Porcentaje infectado: {(total_recuperados/N)*100:.1f}%"),
            html.P("🔴 R₀ > 1: Epidemia creciente" if R0 > 1 else "🟢 R₀ ≤ 1: Epidemia controlada"),
            html.P(f"Retraso pico E→I: {dia_pico - dia_pico_expuestos} días")
        ]
        
        return fig_seir, info_content
        
    except Exception as e:
        error_fig = go.Figure()
        error_fig.add_annotation(
            text=f"Error en la simulación: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        error_fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        error_content = [
            html.H4("Error en la simulación", style={"color": "red"}),
            html.P(f"Error: {str(e)}"),
            html.P("Por favor, revisa los parámetros ingresados.")
        ]
        
        return error_fig, error_content