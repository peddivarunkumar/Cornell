import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import os

# --- Styling Constants for Cornell MBA Theme ---
FONT_FAMILY = 'Montserrat, sans-serif'
COLORS = {
    'primary': '#B31B1B',      # Cornell Red
    'secondary': '#F2F2F2',    # Light Gray
    'text': '#333333',
    'accent': '#003865'         # Dark Blue accent
}

# External stylesheets: Bootstrap + Google Fonts + Animate.css
external_stylesheets = [
    dbc.themes.LUX,
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
]

# Static data for 2016–2024 pulled from each EMR
data = [
    {'year': 2016, 'USA': 126, 'China': 98,  'India': 8,  'EMNC_total': 60,
     'OFDI': 300, 'IFDI': 400, 'Greenfield': 150, 'M_and_A': 200,
     'GDP_share': 45.0, 'GDP_growth': 4.8, 'D_ESG': 50, 'Billionaire_count': 3500},
    {'year': 2017, 'USA': 129, 'China': 108, 'India': 9,  'EMNC_total': 65,
     'OFDI': 320, 'IFDI': 420, 'Greenfield': 160, 'M_and_A': 210,
     'GDP_share': 46.0, 'GDP_growth': 4.5, 'D_ESG': 52, 'Billionaire_count': 3750},
    {'year': 2018, 'USA': 135, 'China': 129, 'India': 10, 'EMNC_total': 72,
     'OFDI': 350, 'IFDI': 450, 'Greenfield': 170, 'M_and_A': 230,
     'GDP_share': 47.0, 'GDP_growth': 4.2, 'D_ESG': 54, 'Billionaire_count': 4000},
    {'year': 2019, 'USA': 137, 'China': 134, 'India': 11, 'EMNC_total': 75,
     'OFDI': 380, 'IFDI': 470, 'Greenfield': 180, 'M_and_A': 240,
     'GDP_share': 48.0, 'GDP_growth': 4.0, 'D_ESG': 56, 'Billionaire_count': 4200},
    {'year': 2020, 'USA': 121, 'China': 124, 'India': 13, 'EMNC_total': 68,
     'OFDI': 400, 'IFDI': 500, 'Greenfield': 160, 'M_and_A': 220,
     'GDP_share': 49.0, 'GDP_growth': 3.0, 'D_ESG': 58, 'Billionaire_count': 4400},
    {'year': 2021, 'USA': 122, 'China': 133, 'India': 15, 'EMNC_total': 78,
     'OFDI': 450, 'IFDI': 520, 'Greenfield': 190, 'M_and_A': 260,
     'GDP_share': 49.5, 'GDP_growth': 3.5, 'D_ESG': 60, 'Billionaire_count': 4600},
    {'year': 2022, 'USA': 129, 'China': 145, 'India': 17, 'EMNC_total': 85,
     'OFDI': 480, 'IFDI': 540, 'Greenfield': 200, 'M_and_A': 280,
     'GDP_share': 49.8, 'GDP_growth': 3.7, 'D_ESG': 61, 'Billionaire_count': 4800},
    {'year': 2023, 'USA': 139, 'China': 144, 'India': 19, 'EMNC_total': 90,
     'OFDI': 520, 'IFDI': 560, 'Greenfield': 210, 'M_and_A': 300,
     'GDP_share': 50.0, 'GDP_growth': 3.9, 'D_ESG': 62, 'Billionaire_count': 5000},
    {'year': 2024, 'USA': 139, 'China': 145, 'India': 20, 'EMNC_total': 95,
     'OFDI': 550, 'IFDI': 580, 'Greenfield': 220, 'M_and_A': 320,
     'GDP_share': 50.2, 'GDP_growth': 4.0, 'D_ESG': 63, 'Billionaire_count': 5200},
]

# Create DataFrame and compute derived metrics
df = pd.DataFrame(data)
# Core ratios
df['EMNC_share'] = df['EMNC_total'] / 500 * 100
# FDI metrics
df['FDI_net'] = df['IFDI'] - df['OFDI']
df['FDI_ratio'] = df['IFDI'] / df['OFDI']
# Greenfield vs M&A share
df['Greenfield_share'] = df['Greenfield'] / (df['Greenfield'] + df['M_and_A']) * 100
df['M_and_A_share'] = df['M_and_A'] / (df['Greenfield'] + df['M_and_A']) * 100
# Intensity metrics
df['D_ESG_per_100eMNC'] = df['D_ESG'] / df['EMNC_total'] * 100
df['Billionaires_per_100eMNC'] = df['Billionaire_count'] / df['EMNC_total'] * 100

# Detailed yearly summaries
summaries = {
    2016: """
**Theme:** China's firms emerge as global heavyweights  
**Key Findings:**  
- Chinese eMNCs exploded on the Fortune 500, rising from 3,883 patents in 1994 to 233,228 in 2014.  
- E20 companies held 37.3% of global patent filings by 2014, up from 14.8% in 1994.  
- India and other EMs showed early signs of expansion.  
**Strategic Take-away:** Build global footprint and brand, double down on in-house R&D and IP protection.
""",
    2017: """
**Theme:** Navigating renewed geopolitical volatility  
**Key Findings:**  
- US/EU outbound flows stabilized post-2016, but rising trade tensions altered investment calculus.  
- eMNCs diversified into non-traditional markets.  
- Digital adoption accelerated as a buffer against cross-border frictions.  
**Strategic Take-away:** Broaden market exposure and deepen policy engagement.
""",
    2018: """
**Theme:** EMNCs driving new value-chain geographies  
**Key Findings:**  
- EM-led value chains captured a growing share of global trade in manufacturing and tech services.  
- Cross-border partnerships surged, especially in tech and infrastructure.  
- Digital ecosystems became critical enablers of EMNC scale.  
**Strategic Take-away:** Invest in proprietary digital platforms and cross-border innovation partnerships.
""",
    2019: """
**Theme:** ESG and strategic alliances as growth levers  
**Key Findings:**  
- ESG considerations moved to board-level priority.  
- FDI strategies pivoted toward constructive engagement with stakeholders.  
- Sustainability goals embedded into governance and performance management.  
**Strategic Take-away:** Integrate ESG metrics into core strategy to unlock funding and partnerships.
""",
    2020: """
**Theme:** A decade of transformation meets COVID-19 resilience tests  
**Key Findings:**  
- Supply-chain disruptions underscored the need for agility and digitalization.  
- EMNCs with digital channels outperformed during lockdowns.  
- "Local+global" models emerged, blending regional hubs with global scale.  
**Strategic Take-away:** Enhance supply-chain agility via digital twins and hybrid local–global models.
""",
    2021: """
**Theme:** ESG performance differentiates EMNC leaders  
**Key Findings:**  
- Top EMNCs set measurable carbon targets and green investments.  
- Social initiatives moved to measurable KPIs.  
- Governance best practices became standard.  
**Strategic Take-away:** Elevate ESG from compliance to competitive advantage through transparent reporting.
""",
    2022: """
**Theme:** Supply-chain realignment and green investments accelerate  
**Key Findings:**  
- GVCs reconfigured for resilience via near-shoring and multi-sourcing.  
- R&D spenders from E20 increased global league-table presence.  
- Major M&A deals involved EM targets, signaling strategic rebalancing.  
**Strategic Take-away:** Localize critical nodes, invest green tech, and use M&A for resilience.
""",
    2023: """
**Theme:** Geopolitical shifts redefine capital flows  
**Key Findings:**  
- Capital flows shifted toward multi-polar EM corridors.  
- EMNCs employed scenario-planning for currency and geopolitical risks.  
- Strategic realignments around digital infra and energy security.  
**Strategic Take-away:** Build scenario-planning frameworks and diversify capital-raising across centers.
""",
    2024: """
**Theme:** AI, digital ecosystems & green R&D reshape the landscape  
**Key Findings:**  
- EM greenfield R&D FDI rose from 23.7% of global total (2020) to 36% (2023).  
- Software & IT dominated new R&D CAPEX (38%).  
- India and China led new announcements; ASEAN and LAC upticks notable.  
**Strategic Take-away:** Scale AI & digital platforms, attract greenfield R&D, and forge tech-transfer partnerships.
"""
}

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                padding: 0;
                width: 100vw;
                overflow-x: hidden;
                font-family: ''' + FONT_FAMILY + ''';
            }
            
            /* Basic container fixes */
            .container-fluid {
                width: 100% !important;
                max-width: none !important;
                padding: 2rem !important;
                margin: 0 !important;
            }
            
            /* Navbar styles */
            .navbar {
                background: linear-gradient(135deg, ''' + COLORS['primary'] + ''', #8B0000) !important;
                padding: 1rem;
                width: 100%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                position: relative;
                overflow: hidden;
            }
            
            .navbar::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: 
                    radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 50%),
                    radial-gradient(circle at 70% 70%, rgba(255,0,0,0.1) 0%, rgba(255,0,0,0) 50%);
                animation: rotate 20s linear infinite;
                z-index: 0;
            }
            
            .navbar::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, 
                    rgba(255,255,255,0.1) 0%,
                    rgba(255,255,255,0) 20%,
                    rgba(255,255,255,0) 80%,
                    rgba(255,255,255,0.1) 100%);
                animation: shimmer 3s ease-in-out infinite;
                z-index: 0;
            }
            
            .navbar-brand {
                color: white !important;
                font-weight: bold;
                transition: all 0.3s ease;
                position: relative;
                z-index: 1;
                text-shadow: 
                    0 0 10px rgba(255,255,255,0.4),
                    0 0 20px rgba(255,255,255,0.3),
                    0 0 30px rgba(255,255,255,0.2),
                    0 0 40px rgba(255,0,0,0.2);
                letter-spacing: 0.5px;
                background: linear-gradient(to right, #fff, #FFD700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: textGlow 2s ease-in-out infinite alternate;
            }
            
            .navbar-brand:hover {
                transform: scale(1.02);
                text-shadow: 
                    0 0 15px rgba(255,255,255,0.6),
                    0 0 30px rgba(255,255,255,0.4),
                    0 0 45px rgba(255,255,255,0.3),
                    0 0 60px rgba(255,0,0,0.3);
                animation: textGlowHover 1s ease-in-out infinite alternate;
            }
            
            @keyframes rotate {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }
            
            @keyframes shimmer {
                0% {
                    transform: translateX(-100%);
                }
                100% {
                    transform: translateX(100%);
                }
            }
            
            @keyframes textGlow {
                0% {
                    text-shadow: 
                        0 0 10px rgba(255,255,255,0.4),
                        0 0 20px rgba(255,255,255,0.3),
                        0 0 30px rgba(255,255,255,0.2),
                        0 0 40px rgba(255,0,0,0.2);
                }
                100% {
                    text-shadow: 
                        0 0 15px rgba(255,255,255,0.5),
                        0 0 25px rgba(255,255,255,0.4),
                        0 0 35px rgba(255,255,255,0.3),
                        0 0 45px rgba(255,0,0,0.3);
                }
            }
            
            @keyframes textGlowHover {
                0% {
                    text-shadow: 
                        0 0 15px rgba(255,255,255,0.6),
                        0 0 30px rgba(255,255,255,0.4),
                        0 0 45px rgba(255,255,255,0.3),
                        0 0 60px rgba(255,0,0,0.3);
                }
                100% {
                    text-shadow: 
                        0 0 20px rgba(255,255,255,0.7),
                        0 0 35px rgba(255,255,255,0.5),
                        0 0 50px rgba(255,255,255,0.4),
                        0 0 65px rgba(255,0,0,0.4);
                }
            }
            
            /* Tab styles */
            .nav-tabs {
                border: none;
                margin-bottom: 1rem;
                background-color: white;
                border-radius: 8px;
                padding: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            .nav-tabs .nav-link {
                border: none;
                color: #495057;
                padding: 0.75rem 1.5rem;
                margin: 0 0.25rem;
                white-space: nowrap;
                border-radius: 6px;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .nav-tabs .nav-link:hover {
                background-color: ''' + COLORS['secondary'] + ''';
                color: ''' + COLORS['primary'] + ''';
                transform: translateY(-2px);
            }
            
            .nav-tabs .nav-link.active {
                color: white;
                background-color: ''' + COLORS['primary'] + ''';
                box-shadow: 0 4px 8px rgba(179, 27, 27, 0.2);
                transform: translateY(-2px);
                font-weight: 600;
            }
            
            /* Card styles */
            .card {
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
                width: 100%;
                padding: 1.5rem;
            }
            
            /* Graph container styles */
            .graph-container {
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                padding: 1rem;
                margin: 1rem 0;
            }
            
            /* Mobile specific styles */
            @media (max-width: 768px) {
                .container-fluid {
                    padding: 1rem !important;
                }
                
                .navbar {
                    padding: 0.5rem;
                }
                
                .navbar-brand {
                    font-size: 1rem;
                }
                
                .nav-tabs {
                    padding: 0.25rem;
                }
                
                .nav-tabs .nav-link {
                    padding: 0.5rem 1rem;
                    margin: 0.125rem;
                    font-size: 0.9rem;
                }
                
                .card {
                    margin: 1rem 0;
                    padding: 1rem;
                }
                
                .row {
                    margin: 0 !important;
                }
                
                .col, [class*="col-"] {
                    padding: 0.5rem !important;
                }
                
                .graph-container {
                    padding: 0.5rem;
                    margin: 0.5rem 0;
                }
            }
            
            /* Plot container fixes */
            .js-plotly-plot, .plot-container {
                width: 100% !important;
            }
            
            .main-svg {
                width: 100% !important;
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

# App Layout
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.Span(
                    "Cornell Emerging Market Multinationals Report Dashboard",
                    className="navbar-brand",
                    style={
                        'whiteSpace': 'normal',
                        'wordBreak': 'break-word',
                        'fontSize': '1.5rem',
                        'fontWeight': 'bold'
                    }
                )
            ],
            fluid=True,
        ),
        color=COLORS['primary'],
        dark=True,
        className="mb-4",
    ),
    dbc.Container(
        [
            # Main Tabs
            dbc.Tabs(
                id="tabs",
                active_tab="overview",
                className="nav-fill w-100 mb-4",
                children=[
                    dbc.Tab(label="Overview", tab_id="overview"),
                    dbc.Tab(label="Trends", tab_id="trends"),
                    dbc.Tab(label="Distribution", tab_id="distribution"),
                    dbc.Tab(label="Macro & ESG", tab_id="macro"),
                    dbc.Tab(label="Correlations", tab_id="correlations"),
                    dbc.Tab(label="Future", tab_id="future"),
                ],
            ),
            dcc.Loading(
                id="loading-content",
                type="circle",
                color=COLORS['primary'],
                children=html.Div(id="content")
            )
        ],
        fluid=True,
        className="px-2 px-md-4"  # Add padding that's smaller on mobile
    )
], className="w-100 h-100 m-0 p-0")

# Callback: Render Content for Tabs
@app.callback(Output("content", "children"), Input("tabs", "active_tab"))
def render_content(active_tab):
    if active_tab == "overview":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Year:", className="h5 mb-2"),
                    dcc.Dropdown(
                        id='overview_year',
                        options=[{'label': y, 'value': y} for y in df.year],
                        value=2024,
                        clearable=False,
                        className="mb-3"
                    ),
                ], xs=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Yearly Summary", className="card-title"),
                            html.Div(id='overview_text', className="overview-text")
                        ]),
                        className="mb-3"
                    )
                ], xs=12, md=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Key Metrics", className="card-title"),
                            html.Div(id='overview_metrics')
                        ]),
                        className="mb-3"
                    )
                ], xs=12, md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Top Countries in Fortune 500", className="card-title"),
                            html.Div(
                                dcc.Graph(
                                    id='overview_countries',
                                    config={'displayModeBar': False, 'responsive': True}
                                ),
                                className="graph-container"
                            )
                        ]),
                        className="mb-3"
                    )
                ], xs=12, md=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("FDI Flows", className="card-title"),
                            html.Div(
                                dcc.Graph(
                                    id='overview_fdi',
                                    config={'displayModeBar': False, 'responsive': True}
                                ),
                                className="graph-container"
                            )
                        ]),
                        className="mb-3"
                    )
                ], xs=12, md=6)
            ])
        ], fluid=True, className="px-3")
    elif active_tab == "trends":
        figs = [
            px.line(df, x='year', y=['USA','China','India'], title="Fortune Global 500 Counts"),
            px.line(df, x='year', y='EMNC_total', title="Total Emerging Market MNCs"),
            px.line(df, x='year', y='Billionaire_count', title="Global Billionaires"),
            px.line(df, x='year', y=['OFDI','IFDI'], title="FDI Flows (bn USD)"),
            px.line(df, x='year', y=['Greenfield','M_and_A'], title="Greenfield vs M&A (bn USD)"),
            px.line(df, x='year', y='FDI_net', title="FDI Net (bn USD)"),
            px.line(df, x='year', y='FDI_ratio', title="FDI Ratio (In/Out)"),
            px.line(df, x='year', y=['Greenfield_share','M_and_A_share'], title="Greenfield vs M&A Share (%)"),
            px.line(df, x='year', y='D_ESG_per_100eMNC', title="D-ESG per 100 eMNCs (%)"),
            px.line(df, x='year', y='Billionaires_per_100eMNC', title="Billionaires per 100 eMNCs (%)")
        ]
        return dbc.Row([dbc.Col(dcc.Graph(figure=fig, config={'displayModeBar': False}), width=12) for fig in figs])
    elif active_tab == "distribution":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Year:", className="h5", style={'fontFamily': FONT_FAMILY}),
                    dcc.Dropdown(
                        id='dist_year',
                        options=[{'label': y, 'value': y} for y in df.year],
                        value=2024,
                        clearable=False,
                        className="mb-3"
                    ),
                ], width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("eMNC Distribution by Country", className="card-title"),
                            html.Div(
                                dcc.Graph(id='pie1', config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("FDI Distribution", className="card-title"),
                            html.Div(
                                dcc.Graph(id='pie2', config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Investment Type Distribution", className="card-title"),
                            html.Div(
                                dcc.Graph(id='pie3', config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Key Metrics Distribution", className="card-title"),
                            html.Div(id='distribution_metrics')
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6)
            ])
        ], fluid=True)
    elif active_tab == "macro":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(
                                dcc.Graph(figure=px.line(df, x='year', y='GDP_share', title="Share of World GDP (%)"), config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(
                                dcc.Graph(figure=px.line(df, x='year', y='GDP_growth', title="Avg GDP Growth (%)"), config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(
                                dcc.Graph(figure=px.line(df, x='year', y='D_ESG', title="D-ESG Score"), config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(
                                dcc.Graph(figure=px.bar(df, x='year', y='EMNC_share', title="eMNCs as % of Fortune 500"), config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6)
            ])
        ], fluid=True)
    elif active_tab == "correlations":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Correlation Heatmap", className="card-title"),
                            html.P("Explore relationships between key metrics", className="text-muted"),
                            html.Div(
                                dcc.Graph(id='correlation_heatmap', config={'displayModeBar': False}),
                                className="graph-container"
                            )
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Strongest Correlations", className="card-title"),
                            html.Div(id='strong_correlations')
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Key Insights", className="card-title"),
                            html.Div(id='correlation_insights')
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp"
                    )
                ], width=12, lg=6)
            ])
        ], fluid=True)
    elif active_tab == "future":
        return dbc.Container([
            # Projections Section
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("2025-2026 Projections", className="card-title", style={'color': COLORS['primary']}),
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("eMNC Growth", className="card-title", style={'color': COLORS['primary']}),
                                                html.P("Projected to reach 120 by 2026", className="card-text"),
                                                html.Small("↑ 26% from 2024", className="text-success"),
                                                html.Div([
                                                    html.Small("2024: 95", className="text-muted"),
                                                    html.Div([
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2025: 108", className="text-muted"),
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2026: 120", className="text-muted")
                                                    ], className="d-flex justify-content-between mt-2")
                                                ])
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=4),
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("ESG Performance", className="card-title", style={'color': COLORS['primary']}),
                                                html.P("Target score of 75 by 2025", className="card-text"),
                                                html.Small("↑ 19% from 2024", className="text-success"),
                                                html.Div([
                                                    html.Small("2024: 63", className="text-muted"),
                                                    html.Div([
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2025: 75", className="text-muted"),
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2026: 82", className="text-muted")
                                                    ], className="d-flex justify-content-between mt-2")
                                                ])
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=4),
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Greenfield Investment", className="card-title", style={'color': COLORS['primary']}),
                                                html.P("Expected to reach 45% share", className="card-text"),
                                                html.Small("↑ 5% from 2024", className="text-success"),
                                                html.Div([
                                                    html.Small("2024: 40%", className="text-muted"),
                                                    html.Div([
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2025: 43%", className="text-muted"),
                                                        html.Span("→", className="mx-2"),
                                                        html.Small("2026: 45%", className="text-muted")
                                                    ], className="d-flex justify-content-between mt-2")
                                                ])
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=4)
                                ])
                            ])
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp border-0",
                        style={'background-color': 'white'}
                    )
                ], width=12),
            ]),
            # Strategic Focus Areas
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Strategic Focus Areas", className="card-title", style={'color': COLORS['primary']}),
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Digital Transformation", className="card-title", style={'color': COLORS['primary']}),
                                                html.Ul([
                                                    html.Li("AI and automation integration"),
                                                    html.Li("Digital platform development"),
                                                    html.Li("Cybersecurity enhancement"),
                                                    html.Li("Data analytics capabilities")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6),
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Sustainability", className="card-title", style={'color': COLORS['primary']}),
                                                html.Ul([
                                                    html.Li("Green technology investments"),
                                                    html.Li("Carbon footprint reduction"),
                                                    html.Li("Sustainable supply chains"),
                                                    html.Li("ESG reporting standards")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Market Expansion", className="card-title", style={'color': COLORS['primary']}),
                                                html.Ul([
                                                    html.Li("Emerging market penetration"),
                                                    html.Li("Strategic partnerships"),
                                                    html.Li("Local market adaptation"),
                                                    html.Li("Cross-border innovation")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6),
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Risk Management", className="card-title", style={'color': COLORS['primary']}),
                                                html.Ul([
                                                    html.Li("Geopolitical scenario planning"),
                                                    html.Li("Currency risk mitigation"),
                                                    html.Li("Supply chain resilience"),
                                                    html.Li("Regulatory compliance")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6)
                                ])
                            ])
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp border-0",
                        style={'background-color': 'white'}
                    )
                ], width=12),
            ]),
            # Key Opportunities
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Key Opportunities", className="card-title", style={'color': COLORS['primary']}),
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Technology & Innovation", className="card-title", style={'color': COLORS['primary']}),
                                                html.P("Leverage AI and digital platforms for scale and efficiency", className="card-text"),
                                                html.Small("Focus Areas:", className="text-muted d-block"),
                                                html.Ul([
                                                    html.Li("AI-driven process optimization"),
                                                    html.Li("Digital ecosystem development"),
                                                    html.Li("Smart manufacturing solutions"),
                                                    html.Li("Data-driven decision making")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6),
                                    dbc.Col([
                                        dbc.Card(
                                            dbc.CardBody([
                                                html.H5("Sustainable Growth", className="card-title", style={'color': COLORS['primary']}),
                                                html.P("Capture green investment opportunities and sustainable practices", className="card-text"),
                                                html.Small("Focus Areas:", className="text-muted d-block"),
                                                html.Ul([
                                                    html.Li("Renewable energy projects"),
                                                    html.Li("Circular economy initiatives"),
                                                    html.Li("Green infrastructure development"),
                                                    html.Li("Sustainable product innovation")
                                                ], className="mb-0")
                                            ]),
                                            class_name="mb-3 border-0",
                                            style={'background-color': COLORS['secondary']}
                                        )
                                    ], width=12, lg=6)
                                ])
                            ])
                        ]),
                        class_name="shadow mb-4 animate__animated animate__fadeInUp border-0",
                        style={'background-color': 'white'}
                    )
                ], width=12),
            ])
        ], fluid=True)
    return ""

# Callback: Update Overview Text
@app.callback(
    Output('overview_text', 'children'),
    Input('overview_year', 'value')
)
def update_overview_text(year):
    summary = summaries.get(year, "")
    # Convert markdown-style formatting to HTML
    summary = summary.replace("**", "")
    return html.Div([
        html.P(line, style={'marginBottom': '1rem'}) for line in summary.split('\n') if line.strip()
    ])

# Callback: Update Overview Metrics
@app.callback(
    Output('overview_metrics', 'children'),
    Input('overview_year', 'value')
)
def update_overview_metrics(year):
    year_data = df[df['year'] == year].iloc[0]
    metrics = [
        ("Total eMNCs", f"{year_data['EMNC_total']}"),
        ("Global GDP Share", f"{year_data['GDP_share']:.1f}%"),
        ("GDP Growth", f"{year_data['GDP_growth']:.1f}%"),
        ("ESG Score", f"{year_data['D_ESG']}"),
        ("Billionaire Count", f"{year_data['Billionaire_count']:,}"),
        ("FDI Net Flow", f"${year_data['FDI_net']}B"),
        ("Greenfield Share", f"{year_data['Greenfield_share']:.1f}%"),
        ("M&A Share", f"{year_data['M_and_A_share']:.1f}%")
    ]
    
    return dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5(label, className="card-title"),
                    html.P(value, className="card-text h4", style={'color': COLORS['primary']})
                ]),
                class_name="mb-3"
            )
        ], width=6) for label, value in metrics
    ])

# Callback: Update Overview Countries
@app.callback(
    Output('overview_countries', 'figure'),
    Input('overview_year', 'value')
)
def update_overview_countries(year):
    year_data = df[df['year'] == year].iloc[0]
    fig = px.bar(
        x=['USA', 'China', 'India'],
        y=[year_data['USA'], year_data['China'], year_data['India']],
        title="",
        labels={'x': 'Country', 'y': 'Count'},
        color=['USA', 'China', 'India'],
        color_discrete_sequence=[COLORS['primary'], COLORS['accent'], '#FFA500']
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        height=300,  # Fixed height for mobile
        xaxis=dict(fixedrange=True),  # Disable zoom
        yaxis=dict(fixedrange=True)   # Disable zoom
    )
    return fig

# Callback: Update Overview FDI
@app.callback(
    Output('overview_fdi', 'figure'),
    Input('overview_year', 'value')
)
def update_overview_fdi(year):
    year_data = df[df['year'] == year].iloc[0]
    fig = px.bar(
        x=['OFDI', 'IFDI'],
        y=[year_data['OFDI'], year_data['IFDI']],
        title="",
        labels={'x': 'Type', 'y': 'Amount (Billion USD)'},
        color=['OFDI', 'IFDI'],
        color_discrete_sequence=[COLORS['primary'], COLORS['accent']]
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        height=300,  # Fixed height for mobile
        xaxis=dict(fixedrange=True),  # Disable zoom
        yaxis=dict(fixedrange=True)   # Disable zoom
    )
    return fig

# Callback: Update Distribution Pie Charts
@app.callback(
    Output('pie1', 'figure'),
    Output('pie2', 'figure'),
    Output('pie3', 'figure'),
    Output('distribution_metrics', 'children'),
    Input('dist_year', 'value')
)
def update_pies(year):
    row = df[df.year == year].iloc[0]
    
    # eMNC Distribution
    fig1 = px.pie(
        names=['USA', 'China', 'India', 'Other'],
        values=[row.USA, row.China, row.India, max(row.EMNC_total-row.USA-row.China-row.India,0)],
        title="",
        color_discrete_sequence=[COLORS['primary'], COLORS['accent'], '#FFA500', COLORS['secondary']]
    )
    fig1.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # FDI Distribution
    fig2 = px.pie(
        names=['OFDI', 'IFDI'],
        values=[row.OFDI, row.IFDI],
        title="",
        color_discrete_sequence=[COLORS['primary'], COLORS['accent']]
    )
    fig2.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Investment Type Distribution
    fig3 = px.pie(
        names=['Greenfield', 'M&A'],
        values=[row.Greenfield, row.M_and_A],
        title="",
        color_discrete_sequence=[COLORS['primary'], COLORS['accent']]
    )
    fig3.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Key Metrics
    metrics = [
        ("eMNC Share of Fortune 500", f"{row.EMNC_share:.1f}%"),
        ("GDP Share", f"{row.GDP_share:.1f}%"),
        ("ESG Score", f"{row.D_ESG}"),
        ("Billionaires per 100 eMNCs", f"{row.Billionaires_per_100eMNC:.1f}")
    ]
    
    metrics_content = dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5(label, className="card-title"),
                    html.P(value, className="card-text h4", style={'color': COLORS['primary']})
                ]),
                class_name="mb-3"
            )
        ], width=6) for label, value in metrics
    ])
    
    return fig1, fig2, fig3, metrics_content

# Callback: Update Correlation Analysis
@app.callback(
    Output('correlation_heatmap', 'figure'),
    Output('strong_correlations', 'children'),
    Output('correlation_insights', 'children'),
    Input('tabs', 'active_tab')
)
def update_correlations(active_tab):
    if active_tab != "correlations":
        return {}, "", ""

    # Select relevant columns for correlation
    cols = [
        'EMNC_total', 'USA', 'China', 'India',
        'OFDI', 'IFDI', 'GDP_share', 'GDP_growth',
        'D_ESG', 'Billionaire_count', 'EMNC_share',
        'FDI_net', 'FDI_ratio', 'Greenfield_share',
        'M_and_A_share', 'D_ESG_per_100eMNC',
        'Billionaires_per_100eMNC'
    ]

    # Calculate correlation matrix
    corr = df[cols].corr()

    # Create heatmap
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu',
        aspect="auto",
        labels=dict(x="Metric", y="Metric", color="Correlation")
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Static narrative and top-5 summary
    intro = (
        "Across 2016–2024, several exceptionally strong relationships stand out "
        "among our strategic metrics. Here are the top five correlations:"
    )
    top5 = [
        "Greenfield vs. M&A share: Perfect inverse (r = –1.00) – as firms shift toward new greenfield projects, they correspondingly pursue fewer acquisitions.",
        "EMNC count vs. EMNC share: Perfect positive (r = +1.00) – since share is derived from count, this validates our ratio calculation.",
        "Inward FDI vs. Billionaire count: Very strong positive (r ≈ +0.999) – higher foreign inflows coincide with rising domestic wealth concentration.",
        "India's Fortune 500 count vs. OFDI: Very strong positive (r ≈ +0.997) – India's outbound investments mirror its growing Fortune 500 presence.",
        "Inward FDI vs. ESG score: Very strong positive (r ≈ +0.995) – global investors favor EMNCs with robust ESG performance."
    ]

    # 1️⃣ Strongest correlations with inline styles
    strong_items = []
    for text in top5:
        title, desc = text.split("–", 1)
        strong_items.append(
            html.Li(
                [
                    html.Strong(title.strip()),
                    html.Span(" – " + desc.strip(), className="text-muted")
                ],
                style={
                    'borderLeft': f"4px solid {COLORS['accent']}",
                    'backgroundColor': '#f2f7fa',
                    'padding': '0.75rem 1rem',
                    'borderRadius': '0.25rem',
                    'marginBottom': '0.5rem'
                }
            )
        )

    strong_correlations_content = html.Div([
        html.P(intro, style={
            'marginBottom': '1rem',
            'fontStyle': 'italic',
            'color': '#555'
        }),
        html.Ul(strong_items, style={'listStyleType': 'none', 'padding': 0})
    ])

    # Key insights
    insights = [
        "Emerging-market multinationals are both drivers and beneficiaries of FDI flows, underscoring their strategic economic role.",
        "Investment type mix matters: the perfect trade-off between greenfield spending and M&A highlights distinct market-entry strategies.",
        "Wealth indicators (billionaire counts) track closely with FDI, reflecting the interplay between capital mobility and domestic wealth creation.",
        "ESG leadership attracts capital: the high correlation with IFDI suggests sustainability performance is increasingly table stakes for global investors.",
        "Foreign direct investment is a cornerstone of wealth creation in emerging markets, evidenced by its near-perfect link to billionaire growth.",
        "ESG excellence has become a critical capital magnet; top sustainability performers draw far more international funding.",
        "The close ESG-wealth connection suggests that sustainable business practices and domestic wealth generation are mutually reinforcing."
    ]

    # 2️⃣ Key insights with inline styles
    insights_items = []
    for insight in insights:
        insights_items.append(
            html.Li(
                html.Strong(insight),
                style={
                    'borderLeft': f"4px solid {COLORS['primary']}",
                    'backgroundColor': '#fbf2f2',
                    'padding': '0.75rem 1rem',
                    'borderRadius': '0.25rem',
                    'marginBottom': '0.5rem'
                }
            )
        )

    insights_content = html.Div([

        html.Ul(insights_items, style={'listStyleType': 'none', 'padding': 0})
    ])

    return fig, strong_correlations_content, insights_content

# Run server
if __name__ == '__main__':
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port, debug=False)