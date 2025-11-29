import dash
from dash import html, dcc, Input, Output, State, callback
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

dash.register_page(__name__, path='/api-cripto', name='API Criptomonedas')

# Layout de la página API de Criptomonedas
layout = html.Div(children=[
    html.Div(className="api-container", children=[
        # Header
        html.Div(className="api-header", children=[
            html.H1("📊 Mercado de Criptomonedas en Tiempo Real", className="api-title"),
            
        ]),
        
        # Panel de controles
        html.Div(className="controls-panel", children=[
            html.Div(className="search-row", children=[
                html.Div(className="input-group", children=[
                    html.Label("Seleccionar Criptomoneda:", className="input-label"),
                    dcc.Dropdown(
                        id="dropdown-cripto",
                        options=[
                            {'label': 'Bitcoin (BTC)', 'value': 'bitcoin'},
                            {'label': 'Ethereum (ETH)', 'value': 'ethereum'},
                            {'label': 'Cardano (ADA)', 'value': 'cardano'},
                            {'label': 'Solana (SOL)', 'value': 'solana'},
                            {'label': 'Polkadot (DOT)', 'value': 'polkadot'},
                            {'label': 'Dogecoin (DOGE)', 'value': 'dogecoin'},
                            {'label': 'XRP (XRP)', 'value': 'ripple'},
                            {'label': 'Litecoin (LTC)', 'value': 'litecoin'}
                        ],
                        value='bitcoin',
                        className="dropdown-field"
                    )
                ]),
                
                html.Div(className="input-group", children=[
                    html.Label("Rango de días:", className="input-label"),
                    dcc.Dropdown(
                        id="dropdown-dias",
                        options=[
                            {'label': '7 días', 'value': 7},
                            {'label': '30 días', 'value': 30},
                            {'label': '90 días', 'value': 90},
                            {'label': '1 año', 'value': 365},
                            {'label': 'Máximo', 'value': 'max'}
                        ],
                        value=30,
                        className="dropdown-field"
                    )
                ]),
                
                html.Div(className="input-group", children=[
                    html.Label("Moneda de referencia:", className="input-label"),
                    dcc.Dropdown(
                        id="dropdown-moneda",
                        options=[
                            {'label': 'USD ($)', 'value': 'usd'},
                            {'label': 'EUR (€)', 'value': 'eur'},
                            {'label': 'GBP (£)', 'value': 'gbp'},
                            {'label': 'JPY (¥)', 'value': 'jpy'}
                        ],
                        value='usd',
                        className="dropdown-field"
                    )
                ])
            ]),
            
            html.Div(className="button-row", children=[
                html.Button(
                    "📈 Obtener Datos",
                    id="btn-obtener-datos",
                    className="btn-generar",
                    n_clicks=0
                ),
                
                html.Button(
                    "🔄 Datos en Tiempo Real",
                    id="btn-tiempo-real",
                    className="btn-secondary",
                    n_clicks=0
                )
            ])
        ]),
        
        # Métricas en tiempo real
        html.Div(id="container-metricas", className="metrics-container", style={'display': 'none'}),
        
        # Gráficas
        html.Div(className="charts-section", children=[
            html.Div(className="chart-row", children=[
                html.Div(className="chart-container", children=[
                    dcc.Graph(id="grafico-precio", config={'displayModeBar': True})
                ]),
                html.Div(className="chart-container", children=[
                    dcc.Graph(id="grafico-volumen", config={'displayModeBar': True})
                ])
            ]),
            
            html.Div(className="chart-row", children=[
                html.Div(className="chart-container-full", children=[
                    dcc.Graph(id="grafico-velas", config={'displayModeBar': True})
                ])
            ])
        ]),
        
        # Información del mercado
        html.Div(id="container-info-mercado", className="market-info")
    ])
])

# Función para obtener datos de CoinGecko API
def obtener_datos_cripto(moneda_id, dias, vs_currency):
    """
    Obtiene datos históricos de criptomonedas de CoinGecko API
    """
    
    # Simulación de datos (para cuando no hay conexión)
    fecha_inicio = datetime.now() - timedelta(days=dias)
    fechas = [fecha_inicio + timedelta(days=i) for i in range(dias)]
    
    # Simular datos de precio (patrón realista)
    precios_simulados = []
    precio_base = 45000 if moneda_id == 'bitcoin' else 3000
    volatilidad = 0.05  # 5% de volatilidad diaria
    
    import random
    random.seed(42)  # Para resultados consistentes
    
    precio_actual = precio_base
    for i in range(dias):
        cambio = random.uniform(-volatilidad, volatilidad)
        precio_actual = precio_actual * (1 + cambio)
        precios_simulados.append(precio_actual)
    
    # Datos simulados
    datos_simulados = {
        'prices': [[int(fecha.timestamp() * 1000), precio] for fecha, precio in zip(fechas, precios_simulados)],
        'market_caps': [[int(fecha.timestamp() * 1000), precio * random.uniform(0.8, 1.2) * 1e6] for fecha, precio in zip(fechas, precios_simulados)],
        'total_volumes': [[int(fecha.timestamp() * 1000), precio * random.uniform(0.5, 2) * 1e5] for fecha, precio in zip(fechas, precios_simulados)]
    }
    
    # Si quieres usar la API real de CoinGecko (gratuita), descomenta:
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{moneda_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': dias,
            'interval': 'daily'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return datos_simulados
    except:
        return datos_simulados
    
    
    return datos_simulados

# Función para crear gráfico de precios
def crear_grafico_precio(datos, vs_currency):
    if not datos or 'prices' not in datos:
        return go.Figure()
    
    df = pd.DataFrame(datos['prices'], columns=['timestamp', 'price'])
    df['fecha'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['fecha'],
        y=df['price'],
        mode='lines',
        name='Precio',
        line=dict(color='#00D4AA', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 170, 0.1)',
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Precio:</b> %{y:,.2f} ' + vs_currency.upper() + '<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Evolución del Precio</b>',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis_title='Fecha',
        yaxis_title=f'Precio ({vs_currency.upper()})',
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        height=400,
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    return fig

# Función para crear gráfico de volumen
def crear_grafico_volumen(datos, vs_currency):
    if not datos or 'total_volumes' not in datos:
        return go.Figure()
    
    df = pd.DataFrame(datos['total_volumes'], columns=['timestamp', 'volume'])
    df['fecha'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['fecha'],
        y=df['volume'],
        name='Volumen',
        marker_color='#FF6B6B',
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Volumen:</b> %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Volumen de Trading</b>',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis_title='Fecha',
        yaxis_title='Volumen',
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        height=400,
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    return fig

# Función para crear gráfico de velas (OHLC)
def crear_grafico_velas(datos, vs_currency):
    if not datos or 'prices' not in datos:
        return go.Figure()
    
    df = pd.DataFrame(datos['prices'], columns=['timestamp', 'price'])
    df['fecha'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Simular datos OHLC a partir de los precios de cierre
    df['open'] = df['price'] * 0.98  # Apertura ligeramente menor
    df['high'] = df['price'] * 1.05  # Máximo más alto
    df['low'] = df['price'] * 0.95   # Mínimo más bajo
    df['close'] = df['price']        # Cierre igual al precio
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df['fecha'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Precio OHLC',
        increasing_line_color='#00D4AA',
        decreasing_line_color='#FF6B6B'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Gráfico de Velas (OHLC)</b>',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis_title='Fecha',
        yaxis_title=f'Precio ({vs_currency.upper()})',
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        height=500,
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis_rangeslider_visible=False
    )
    
    return fig

# Callbacks
@callback(
    [Output('container-metricas', 'children'),
     Output('grafico-precio', 'figure'),
     Output('grafico-volumen', 'figure'),
     Output('grafico-velas', 'figure'),
     Output('container-info-mercado', 'children')],
    [Input('btn-obtener-datos', 'n_clicks'),
     Input('btn-tiempo-real', 'n_clicks')],
    [State('dropdown-cripto', 'value'),
     State('dropdown-dias', 'value'),
     State('dropdown-moneda', 'value')],
    prevent_initial_call=True
)
def actualizar_datos(n_clicks_obtener, n_clicks_tiempo_real, moneda_id, dias, vs_currency):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    # Obtener datos
    datos = obtener_datos_cripto(moneda_id, dias, vs_currency)
    
    # Crear métricas
    if datos and 'prices' in datos:
        precios = [price for _, price in datos['prices']]
        precio_actual = precios[-1] if precios else 0
        precio_inicial = precios[0] if precios else 0
        cambio_porcentaje = ((precio_actual - precio_inicial) / precio_inicial * 100) if precio_inicial else 0
        
        metricas = html.Div([
            html.H3("📊 Métricas en Tiempo Real", className="metrics-title"),
            html.Div([
                html.Div([
                    html.P(f"${precio_actual:,.2f}", className="metric-value"),
                    html.P("Precio Actual", className="metric-label")
                ], className="metric-card"),
                html.Div([
                    html.P(f"{cambio_porcentaje:+.2f}%", 
                          className="metric-value", 
                          style={'color': '#00D4AA' if cambio_porcentaje >= 0 else '#FF6B6B'}),
                    html.P("Cambio Total", className="metric-label")
                ], className="metric-card"),
                html.Div([
                    html.P(f"{dias} días", className="metric-value"),
                    html.P("Período Analizado", className="metric-label")
                ], className="metric-card")
            ], className="metrics-grid")
        ])
    else:
        metricas = html.Div("No se pudieron obtener los datos")
    
    # Crear gráficas
    fig_precio = crear_grafico_precio(datos, vs_currency)
    fig_volumen = crear_grafico_volumen(datos, vs_currency)
    fig_velas = crear_grafico_velas(datos, vs_currency)
    
    # Información del mercado
    info_mercado = html.Div([
        html.H3("💡 Información del Mercado"),
        dcc.Markdown(f"""
**{moneda_id.upper()}** - Análisis de {dias} días en {vs_currency.upper()}

**Características:**
- **Volatilidad:** Alta en criptomercados
- **Liquidez:** Depende del volumen de trading
- **Tendencia:** {'Alcista' if cambio_porcentaje > 0 else 'Bajista'}

**Recomendaciones:**
- Siempre haz tu propia investigación (DYOR)
- Diversifica tu portfolio
- Invierto solo lo que estés dispuesto a perder
        """)
    ], className="market-info-content")
    
    return metricas, fig_precio, fig_volumen, fig_velas, info_mercado

# Callback para mostrar métricas
@callback(
    Output('container-metricas', 'style'),
    Input('btn-obtener-datos', 'n_clicks'),
    prevent_initial_call=True
)
def mostrar_metricas(n_clicks):
    if n_clicks:
        return {'display': 'block'}
    return {'display': 'none'}
