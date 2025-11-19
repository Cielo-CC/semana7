import plotly.graph_objects as go
import numpy as np

def generar_graf_pob_exp(P0, r, t_max):
    # Generar los valores de tiempo
    t = np.linspace(0, t_max, 100)
    
    # Calcular la población usando el modelo exponencial
    P = P0 * np.exp(r * t)
    
    # Crear el scatter plot
    trace = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        line=dict(
            dash='dot',
            color='black',
            width=2
        ),
        marker=dict(
            color='blue',
            symbol='square',
            size=6
        ),
        name=f'Población P(t) = {P0} * e^({r}t)',
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )
    
    # Crear la figura
    fig = go.Figure(data=[trace])
    
    fig.update_layout(
        title=dict(
            text='<b>Crecimiento Exponencial de la Población</b>',
            font=dict(size=18, color='#2c3e50', family='Outfit'),
            x=0.5,
            y=1
        ),
        xaxis_title='<b>Tiempo (t)</b>',
        yaxis_title='<b>Población P(t)</b>',
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        font=dict(family='Outfit', size=12, color='#34495e'),
        height=450,
        showlegend=True,
        legend=dict(
            orientation = "h",
            yanchor="bottom",
            y=1.02
        )
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='#d7dee3',
        zeroline=True, zerolinewidth=2, zerolinecolor='#919597',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#d7dee3',
        zeroline=True, zerolinewidth=2, zerolinecolor="#919597",
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    return fig


def generar_grafico_logistico(P0, r, K, t_max):
    t = np.linspace(0, t_max, 200)  
    
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
        name=f'Población P(t)',
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
        name=f'Capacidad de Carga K = {K}',
        hovertemplate='<b>Capacidad de Carga:</b> %{y:.0f}<extra></extra>'
    )
    
    fig = go.Figure(data=[trace_logistico, trace_capacidad])
    
    fig.update_layout(
        title=dict(
            text='<b>Crecimiento Logístico de la Población</b>',
            font=dict(size=18, color='#2c3e50', family='Outfit'),
            x=0.5,
            y=1
        ),
        xaxis_title='<b>Tiempo (t)</b>',
        yaxis_title='<b>Población P(t)</b>',
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor='white',
        plot_bgcolor='#f8f9fa',
        font=dict(family='Outfit', size=12, color='#34495e'),
        height=450,
        showlegend=True,
        legend=dict(
            orientation = "h",
            yanchor="bottom",
            y=1.02
        )
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="#d7dee3",
        zeroline=True, zerolinewidth=2, zerolinecolor='#919597',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#d7dee3',
        zeroline=True, zerolinewidth=2, zerolinecolor='#919597',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    return fig