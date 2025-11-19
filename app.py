import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Inicializar la aplicación Dash
app = Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Configuración para ocultar la barra inferior
app.config.suppress_callback_exceptions = True

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Cielo Zacarias - Portfolio</title>
        {%favicon%}
        {%css%}
        <style>
            ._dash-loading, .dash-debug-menu, .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout principal
app.layout = html.Div([
    # Header
    html.Header(className='app-header', children=[
        html.H1("Técnicas de Modelamiento Matemático")
    ]),
    
    # Navegación
    html.Nav(className='navigation', children=[
        html.Div(className='nav-container', children=[
            html.Div(className='nav-links', children=[
                dcc.Link("Inicio", href='/', className='nav-link'),
                dcc.Link("Exponencial", href='/exponencial', className='nav-link'),
                dcc.Link("Logístico", href='/logistico', className='nav-link'),
                dcc.Link("Exponencial Interactivo", href='/exponencial-interactivo', className='nav-link'),
                dcc.Link("Logístico Interactivo", href='/logistico-interactivo', className='nav-link'),
                dcc.Link("Campo Vectorial", href='/campo-vectorial', className='nav-link'),
                dcc.Link("Modelo SIR", href='/modelo-sir', className='nav-link'),
                dcc.Link("Modelo SEIR", href='/modelo-seir', className='nav-link')
            ])
        ])
    ]),
    
    # Contenido de las páginas
    html.Main(className='main-content', children=[
        dash.page_container
    ])
], className='app-container')

if __name__ == '__main__':
    print("🚀 Servidor iniciado en: http://127.0.0.1:8050")
    # CAMBIA ESTA LÍNEA - desactiva las herramientas de desarrollo
    app.run(
        debug=True,  # Puedes mantener debug=True si quieres
        dev_tools_ui=False,        # ← Esto elimina la toolbar
        dev_tools_props_check=False, # ← Esto también ayuda
        dev_tools_serve_dev_bundles=False
    )