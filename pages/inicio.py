import dash
from dash import html

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div(className='cv-container', children=[


    # ===== SOBRE MÍ =====
    html.Section(className='about-section', children=[
        html.Div(className='about-card', children=[
            html.Img(src='../assets/images/cielo.jpg', alt="Cielo Zacarias", className='about-img'),
            html.Div(className='about-text', children=[
                html.H2("Cielo Zacarias"),
                html.P("Computación Científica ·· UNMSM", className='about-sub'),
                html.P([
                    "Desde que ingresé a la ",
                    html.Strong("Facultad de Ciencias Matemáticas"),
                    " he combinado estudios, tecnología y representación estudiantil. Participé como ",
                    html.Strong("voluntaria en el Concurso de Matemática Binaria"),
                    " para promover la ciencia en colegios y hoy soy ",
                    html.Strong("Consejera Universitaria"),
                    " de la UNMSM. Me apasiona la ",
                    html.Strong("inteligencia artificial, el desarrollo de software y la innovación social"),
                    ". Mi objetivo es usar la tecnología para resolver problemas reales y liderar proyectos que generen impacto positivo."
                ]),
                html.Div(className='about-tags', children=[
                    html.Span("🎓 Consejera Universitaria"),
                    html.Span("📊 Matemática Binaria"),
                
                    html.Span("🌎 Impacto Social")
                ])
            ])
        ])
    ]),

     # ===== PERFIL ACADÉMICO =====
html.Section(className='profile-section', children=[
    html.H3("📊 Perfil Académico", className='section-title'),
    html.Div(className='academic-grid', children=[
        html.Div(className='academic-item', children=[
            html.Div("🏛️", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Universidad"),
                html.P("UNMSM")
            ])
        ]),
        html.Div(className='academic-item', children=[
            html.Div("📚", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Facultad"),
                html.P("Ciencias Matemáticas")
            ])
        ]),
        html.Div(className='academic-item', children=[
            html.Div("💻", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Especialidad"),
                html.P("Computación Científica")
            ])
        ]),
        html.Div(className='academic-item', children=[
            html.Div("🔄", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Ciclo Actual"),
                html.P("6° ciclo")
            ])
        ]),
        html.Div(className='academic-item', children=[
            html.Div("🎯", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Carrera Técnica"),
                html.P("Técnico en Operación de Computadoras")
            ])
        ]),
        html.Div(className='academic-item', children=[
            html.Div("⭐", className='academic-icon'),
            html.Div(className='academic-info', children=[
                html.H4("Formación Complementaria"),
                html.P("Especialización técnica en sistemas")
            ])
        ])
    ])
]),

        # ===== LIDERAZGO =====
        html.Section(className='leadership-section', children=[
            html.H3("🏆 Liderazgo y Participación", className='section-title'),
            html.Div(className='leadership-grid', children=[
                html.Div(className='leadership-item', children=[
                    html.Div("⭐", className='leadership-icon'),
                    html.Div(className='leadership-info', children=[
                        html.H4("Consejera Universitaria"),
                        html.P("UNMSM (Junio 2025 - Presente)"),
                        html.P("Representación estudiantil y gestión universitaria")
                    ])
                ]),
                html.Div(className='leadership-item', children=[
                    html.Div("❤️", className='leadership-icon'),
                    html.Div(className='leadership-info', children=[
                        html.H4("Voluntaria"),
                        html.P("Concurso de Matemática Binaria"),
                        html.P("Promoción científica en colegios")
                    ])
                ])
            ])
        ]),

# ===== HABILIDADES =====
        html.Section(className='skills-section', children=[
            html.H3("🎯 Habilidades e Intereses", className='section-title'),
            html.Div(className='skills-grid', children=[
                html.Div(className='skills-category', children=[
                    html.H4("💻 Programación"),
                    html.Ul(className='skills-list', children=[
                        html.Li("JavaScript"),
                        html.Li("PHP"),
                        html.Li("MySQL"),
                        html.Li("HTML/CSS")
                    ])
                ]),
                html.Div(className='skills-category', children=[
                    html.H4("🚀 Áreas de Interés"),
                    html.Ul(className='skills-list', children=[
                        html.Li("Inteligencia Artificial"),
                        html.Li("Desarrollo de Software"),
                        html.Li("Innovación Social")
                    ])
                ]),
                html.Div(className='skills-category', children=[
                    html.H4("🌟 Habilidades Profesionales"),
                    html.Ul(className='skills-list', children=[
                         html.Li("Liderazgo Estudiantil"),
                        html.Li("Trabajo en Equipo"),
                        html.Li("Resolución de Problemas"),
                        html.Li("Comunicación Efectiva"),
                        html.Li("Gestión de Proyectos")
                    ])
                ]),
                html.Div(className='skills-category', children=[
                    html.H4("📈 Enfoques de Trabajo"),
                    html.Ul(className='skills-list', children=[
                         html.Li("Pensamiento Algorítmico"),
                        html.Li("Análisis Matemático"),
                        html.Li("Desarrollo Iterativo"),
                        html.Li("Aprendizaje Continuo"),
                          html.Li("Innovación Práctica")
                    ])
            ])
            ])
        ]),
        
        # ===== PROYECTOS =====
        html.Section(className='timeline-section', children=[
            html.H3("💻 Proyectos Técnicos", className='section-title'),
            html.Div(className='timeline', children=[
                html.Div(className='timeline-item', children=[
                    html.Div("Ciclo 5", className='tl-ciclo'),
                    html.Div(className='tl-content', children=[
                        html.H4("🍽️ Sistema Web para Restaurante"),
                        html.P("Plataforma completa con gestión de pedidos y administración"),
                        html.Ul(className='tech-list', children=[
                            html.Li("Base de datos MySQL"),
                            html.Li("Paneles para clientes y personal"),
                            html.Li("Tecnologías: PHP, Bootstrap, MySQL")
                        ])
                    ])
                ]),
                html.Div(className='timeline-item', children=[
                    html.Div("Ciclo 4", className='tl-ciclo'),
                    html.Div(className='tl-content', children=[
                        html.H4("🔗 BlockLedger Lite"),
                        html.P("Simulador avanzado de blockchain con interfaz mejorada"),
                        html.Ul(className='tech-list', children=[
                            html.Li("Algoritmo de prueba de trabajo"),
                            html.Li("Validación de nodos"),
                            html.Li("Proyecto destacado en Estructuras de Datos"),
                            html.Li("Tecnologías: HTML, CSS, JavaScript, JSON")
                        ])
                    ])
                ]),
                html.Div(className='timeline-item', children=[
                    html.Div("Ciclo 3", className='tl-ciclo'),
                    html.Div(className='tl-content', children=[
                        html.H4("⛓️ Simulador de Blockchain"),
                        html.P("Prototipo educativo sobre tecnología blockchain"),
                        html.Ul(className='tech-list', children=[
                            html.Li("Minado y validación"),
                            html.Li("Registro de transacciones"),
                            html.Li("Tecnologías: HTML, CSS, JavaScript")
                        ])
                    ])
                ])
            ])
        ]),

        

])