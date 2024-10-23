#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os
import requests

# Google Drive file ID
file_id = '16lramFSvU4lzshUUMskGzfAi488IibiO'
download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

# Download the file
response = requests.get(download_url)
open('df_unique.csv', 'wb').write(response.content)

# Load the CSV into a DataFrame
df_unique = pd.read_csv('df_unique.csv')
paper_counts = pd.read_csv('assets/paper_counts.csv')

spektrum = ['#F2A604', '#ED90AE', '#59A689', '#5DAA53', '#0A4E6B', '#232323']

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Use a single dark theme for all components
dark_theme = {
    'background': "#20272D",  # Darkest color for the background
    'text': "#FFEACF",  # Lightest color for the text
}

sidebar = html.Div(
    [
        html.Hr(style={'border': '1px solid #E09351FF', 'width': '85%', 'margin': '10px auto', 'opacity': '0.7'}),
        html.P("plots & graphs:", id='plots-text', style={'textAlign': 'center', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text']}),  
        dcc.Dropdown(
            id='page-selector-dropdown',
            options=[
                {'label': 'Dark Matter Models', 'value': '/page-1'},
                {'label': 'Particles', 'value': '/page-2'},
                {'label': 'Gravity', 'value': '/page-3'},
                {'label': 'Theories', 'value': '/page-4'},
                {'label': 'Telescopes', 'value': '/page-5'},
                {'label': 'Detectors', 'value': '/page-6'},
                {'label': 'Colliders', 'value': '/page-7'},
                {'label': 'Inferences', 'value': '/page-8'},
                {'label': 'Methods', 'value': '/page-9'},
                {'label': 'Mass range', 'value': '/page-10'},
            ],
            value='/page-1',  # Default value
            className='custom-dropdown',  # Apply custom CSS class
            style={'color': dark_theme['text'], 'backgroundColor': dark_theme['background']}  # Dropdown's visible part
        ),
        html.Hr(style={'border': '1px solid #E09351FF', 'width': '85%', 'margin': '10px auto', 'opacity': '0.7'}),
        
        # Clickable "About" text added
        dcc.Link(
            "about the project",  # Display text
            href='/about',  # This is the URL it will update to when clicked
            style={'textAlign': 'center', 'display': 'block', 'marginTop': '20px', 'color': dark_theme['text'], 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400'}
        ),
    ],
    id='sidebar',
    style={'width': '20%', 'position': 'fixed', 'height': '100%', 'backgroundColor': dark_theme['background']}
)


# Header
header = html.Div(
    html.H1("d a r k . m a t t e r . r e s e a r c h . d a t a", id='header-title', style={'textAlign': 'center', 'color': dark_theme['text']}),
    style={'backgroundColor': dark_theme['background'], 'padding': '0px'}
)

# Page layouts without light/dark mode switching
def page_1_layout():
    return html.Div([

        html.H2('Dark Matter Models', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('1. Top 20 most frequently referenced dark matter models', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        # Add explanatory text here using html.P
        html.P(
            'Grid plot showing the 20 most frequently referred dark matter models. Frequency is based on counting uses in every bibcode (i.e. unique bibliographic identifier). '
            'The y-axis is logarithmic.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'center', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='top20-dm-models-img', src='assets/top20_dm_models_grid.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('2. Prevalence of Dark Matter Models in Papers Over Time', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        # Add explanatory text here using html.P
        html.P(
            'Boxplot showing when the frequency peaks (i.e. when the model was at the hight of popularity). Error bars showing first and most recent references.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'center', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='pop-dm-models-img', src='assets/pop_dm_models.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H3('3. Mass Range Coverage for Dark Matter Models', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        # Add explanatory text here using html.P
        html.P(
            'Plot of the mass range (in GeV) covered by the models. For macho´s and pbh I have added solar mass after their labels in parenthesis.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'center', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='mass-dm-models-img', src='assets/mass_dm_models.svg', style={'width': '100%', 'height': 'auto'}),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H3("4. Interactive Plots", style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        # Add explanatory text here using html.P
        html.P(
            'Charts showing the proportions of models covered in the literature. Grouped by particles-based, exotic, supersymmetric, and interaction-based. Hover to see paper count for respective model',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'center', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Div(dcc.Graph(id='sunburst-dm-models'), style={'display': 'flex', 'justifyContent': 'center'}),
        html.Div(dcc.Graph(id='treemap-dm-models'), style={'display': 'flex', 'justifyContent': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_2_layout():
    return html.Div([
        html.H2('Particles', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='particles-img', src='assets/top_20_particles_grid_dark.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_3_layout():
    return html.Div([
        html.H2('Gravitational phenomena', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='gravity-img', src='assets/top15_gravity_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='gravity-all-img', src='assets/all_gravity_terms_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_4_layout():
    return html.Div([
        html.H2('Theories', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='theory-img', src='assets/top20_theory_grid_dark.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_5_layout():
    return html.Div([
        html.H2('Telescopes', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='telescopes-img', src='assets/top20_telescopes_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_6_layout():
    return html.Div([
        html.H2('Detectors', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='detector-img', src='assets/top20_detectors_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_7_layout():
    return html.Div([
        html.H2('Colliders', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='colliders-img', src='assets/top20_colliders_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_8_layout():
    return html.Div([
        html.H2('Inferences', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='inferences-img', src='assets/top20_inferences_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_9_layout():
    return html.Div([
        html.H2('Methods', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='methods-img', src='assets/top20_methods_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_10_layout():
    return html.Div([
        html.H2('Mass range', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Use frequency of mass/energy expressions over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Div(
            html.Img(id='mass-img', src='assets/mass_range.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_about_layout():
    return html.Div([
        html.H2('About the project', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

# Main layout
app.layout = html.Div(id='main-div', style={'fontFamily': 'DejaVu Sans Mono', 'backgroundColor': dark_theme['background']}, children=[
    dcc.Location(id='url', refresh=False),  # Track the URL for page routing
    header,
    sidebar,
    html.Div(id='page-content',
             style={'marginTop': '80px', 'padding': '20px', 'backgroundColor': dark_theme['background']}),  # Dynamic content area
    html.Footer(
            "© 2024 Simon Allzén | s.allzen@uva.nl",  # Footer text
            id='footer'
        )
])

# URL routing callback
@app.callback(Output('url', 'pathname'), [Input('page-selector-dropdown', 'value')])
def update_url_from_dropdown(selected_page):
    return selected_page

# Callback to display the appropriate page content
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout()
    elif pathname == '/page-2':
        return page_2_layout()
    elif pathname == '/page-3':
        return page_3_layout()
    elif pathname == '/page-4':
        return page_4_layout()
    elif pathname == '/page-5':
        return page_5_layout()
    elif pathname == '/page-6':
        return page_6_layout()
    elif pathname == '/page-7':
        return page_7_layout()
    elif pathname == '/page-8':
        return page_8_layout()
    elif pathname == '/page-9':
        return page_9_layout()
    elif pathname == '/page-10':
        return page_10_layout()
    elif pathname == '/about':
        return page_about_layout()


    else:
        return html.Div([
            html.H1("404 - Page Not Found", style={'textAlign': 'center', 'color': 'red'}),
            html.P("The page you are looking for does not exist.", style={'textAlign': 'center'}),
        ])

# Callback to update the plots dynamically
@app.callback(
    [Output('sunburst-dm-models', 'figure'), Output('treemap-dm-models', 'figure')],
    Input('url', 'pathname')
)
def update_plots(pathname):
    # Sunburst plot (static)
    fig_sunburst = px.sunburst(
        paper_counts, path=['dm_category', 'dm_models'], values='paper_count',
        color_discrete_sequence=spektrum
    )
    fig_sunburst.update_layout(
        font=dict(family="DejaVu Sans Mono", color=dark_theme['text']),
        plot_bgcolor=dark_theme['background'],
        paper_bgcolor=dark_theme['background'],
        margin=dict(t=50, l=25, r=25, b=25)
    )

    # Treemap plot (static)
    fig_treemap = px.treemap(
        paper_counts, path=['dm_category', 'dm_models'], values='paper_count',
        color='paper_count', color_continuous_scale='ylgn'
    )
    fig_treemap.update_layout(
        font=dict(family="DejaVu Sans Mono", color=dark_theme['text']),
        plot_bgcolor=dark_theme['background'],
        paper_bgcolor=dark_theme['background'],
        margin=dict(t=50, l=25, r=25, b=25)
    )

    return fig_sunburst, fig_treemap

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8054))
    app.run_server(debug=False, host='0.0.0.0', port=port)
