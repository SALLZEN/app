#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os
import requests
import random
# Google Drive file ID
file_id = '16lramFSvU4lzshUUMskGzfAi488IibiO'
skeleton_id = '1WQgTgy5TXD3fDkFtJks5cxo75JUeO1m6'
download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
download_skeleton = f'https://drive.google.com/uc?export=download&id={skeleton_id}'

# Download the file
response = requests.get(download_url)
skeleton_response = requests.get(download_skeleton)
open('df_unique.csv', 'wb').write(response.content)
open('skeleton.pkl', 'wb').write(skeleton_response.content)

# Load the CSV into a DataFrame
df = pd.read_pickle('skeleton.pkl')
df_unique = pd.read_csv('df_unique.csv')
paper_counts = pd.read_csv('assets/paper_counts.csv')


# Plot codes:
# downloads vs. citations                                                                                           -> PLOT <-
# Define custom color
custom_color = '#F2A604'
scatter_fig = px.scatter(
    df,
    x='downloads',
    y='citations',
    hover_data=['title', 'first_author', 'year'],
    title='Relationship Between Citations and Downloads',
    labels={'downloads': 'Downloads', 'citations': 'Citations'},
    opacity=0.5,
)
scatter_fig.update_layout(
    font=dict(
        family="DejaVu Sans Mono",
        size=12,
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=18,
        color='#fff8e8',
    ),
    plot_bgcolor='#20272d',
    paper_bgcolor='#20272d',
    width=1000,
    height=700,
    xaxis=dict(
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        type='log'
    ),
    yaxis=dict(
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        type='log',
    ),
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    )
)
scatter_fig.update_traces(
    marker=dict(
        color=custom_color,
        size=7,
        line=dict(
            width=0.2,
            color='#20272d'
        )
    )
)

#dark matter models & research trends
spektrum = ['#FFF8E8', '#FCDCA4', '#FDBF7F','#FCB57A', '#EEB57C', '#EE9D6D', '#ECD305',  '#FCC405', '#ECB13B','#F2A604','#DC8334', '#CE781F', '#EB7B13', '#E46A26', '#DC670B','#EC5B1D','#B64810', '#965C02',  '#805C08', '#784304','#893B04','#943D0C', '#8E4709','#ED90AE',  '#F0817E', '#9E6171', '#D58487','#976264', '#A5D5CA',  '#A4D4AC', '#59A689','#56AA93','#076166', '#AED3D4',  '#65D4CC', '#5E9E95', '#314D5A','#0A4E6B', '#343E49','#C3CC9C', '#89A85A',  '#5DAA53', '#0D7249', '#3C5531','#746C0B', '#41502B']
random.shuffle(spektrum)


category_data = df[['year', 'theory', 'particles', 'gravity', 'detectors', 'colliders', 'dm_models', 'telescopes', 'stellar_objects', 'methods', 'inferences']].copy()
category_data['dm_models'] = category_data['dm_models'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
category_data['category'] = category_data['dm_models']
category_data['research focus'] = None

category_data.loc[category_data['particles'].notnull(), 'research focus'] = 'Particles'
category_data.loc[category_data['gravity'].notnull(), 'research focus'] = 'Gravitational phenomena'
category_data.loc[category_data['detectors'].notnull(), 'research focus'] = 'Detectors'
category_data.loc[category_data['theory'].notnull(), 'research focus'] = 'Theories'
category_data.loc[category_data['colliders'].notnull(), 'research focus'] = 'Colliders'
category_data.loc[category_data['stellar_objects'].notnull(), 'research focus'] = 'Stellar Objects'
category_data.loc[category_data['methods'].notnull(), 'research focus'] = 'Methods'
category_data.loc[category_data['inferences'].notnull(), 'research focus'] = 'Inferences'
category_data.loc[category_data['telescopes'].notnull(), 'research focus'] = 'Telescopes'

category_data = category_data.dropna(subset=['category', 'research focus'])
grouped_data = category_data.groupby(['year', 'category', 'research focus']).size().reset_index(name='counts')


fig_1 = px.bar(
    grouped_data,
    x='year',
    y='counts',
    color='category',
    facet_row='research focus',
    labels={'year': 'Year', 'counts': 'Number of papers', 'category': 'Dark Matter Models'},
    color_discrete_sequence=spektrum
)

fig_1.update_layout(
    font=dict(family="DejaVu Sans Mono", size=12, color='#fff8e8'),
    plot_bgcolor='#20272d',
    paper_bgcolor='#20272d',
    width=1200,
    height=3400,
    xaxis=dict(
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)'
    ),
    yaxis=dict(
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)'
    ),
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    ),
    showlegend=False
)

fig_1.update_yaxes(type='log', matches='y', gridcolor='rgba(255, 255, 255, 0.2)', linecolor='rgba(255, 255, 255, 0.5)')
fig_1.update_xaxes(
    matches='x',
    showticklabels=True,
    title_font=dict(color='#fff8e8'),
    tickfont=dict(color='#fff8e8'),
    gridcolor='rgba(255, 255, 255, 0.2)',
    linecolor='rgba(255, 255, 255, 0.5)'
)
fig_1.for_each_annotation(lambda a: a.update(textangle=90, font=dict(color='#fff8e8')))



spektrum_2 = ['#F2A604', '#ED90AE', '#59A689', '#5DAA53', '#0A4E6B', '#232323']

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Use a single dark theme for all components
dark_theme = {
    'background': "#20272D",  # Darkest color for the background
    'text': "#FFF8E8",  # Lightest color for the text
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
                {'label': 'Stellar objects', 'value': '/page-10'},
                {'label': 'Mass range', 'value': '/page-11'},
                {'label': 'Metrics', 'value': '/page-12'},
                {'label': 'Authors', 'value': '/page-13'},
                {'label': 'arXiv', 'value': '/page-14'},
                {'label': 'Keywords', 'value': '/page-15'},
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
    html.H4("dark matter research data", id='header-title', style={'textAlign': 'left', 'color': dark_theme['text']}),
    style={'backgroundColor': dark_theme['background'], 'padding': '0px'}
)

# Page layouts without light/dark mode switching
def page_1_layout():
    return html.Div([
# PLOT 1        
html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

html.H2('Dark Matter Models', style={
    'fontFamily': 'DejaVu Sans Mono', 
    'fontWeight': '400', 
    'color': dark_theme['text'], 
    'textAlign': 'left',  # Change to left justification
    'marginLeft': '10%'  # Optional: Align text with other elements
}),

html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

html.H1('1.', style={
    'fontFamily': 'DejaVu Sans Mono', 
    'fontWeight': '400', 
    'color': dark_theme['text'], 
    'textAlign': 'left',  # Change to left justification
    'fontSize': '3em',
    'marginLeft': '10%'  # Optional alignment for indentation
}),

html.H3('Top 20 most frequently referenced dark matter models', style={
    'fontFamily': 'DejaVu Sans Mono', 
    'fontWeight': '400', 
    'color': dark_theme['text'], 
    'textAlign': 'left',  # Change to left justification
    'marginLeft': '10%'  # Optional alignment
}),

# Explanatory text with left justification
html.P(
    'The plot below is a series of stacked bar charts. Every bar chart represents one research focus, and every bar contains the proportions of dark matter models prevalent yearly in that research focus. Hover with cursor to see specific dark matter models and its paper count for the year.',
    style={
        'fontFamily': 'DejaVu Sans Mono',
        'color': dark_theme['text'], 
        'textAlign': 'left',  # Change to left justification
        'padding': '5px', 
        'lineHeight': '1',
        'fontSize': '12px',
        'width': '80%',  
        'margin': '0 auto',
        'marginLeft': '10%'  # Optional alignment for indentation
    }
),

        dcc.Graph(id='barplot-dm-models', figure=fig_1, style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),

# PLOT 2
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%'  # Optional alignment for indentation
        }),
        html.H3('Top 20 most frequently referenced dark matter models', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        html.P(
            'Grid plot showing the 20 most frequently referred dark matter models. Frequency is based on counting uses in every bibcode (i.e. unique bibliographic identifier). '
            'The y-axis is logarithmic.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='top20-dm-models-img', src='assets/top20_dm_models_grid.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
# PLOT 3
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('3.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%'
        }),
        html.H3('Top 20 Dark Matter Models by Citations', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        html.P(
            'The top 20 dark matter models in terms of citations of papers referring to them. ',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='citations-dm-models-img', src='assets/dm_models_vs_citations.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
        
#PLOT 4
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('4.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%'
        }),
        html.H3('Prevalence of Dark Matter Models in Papers Over Time', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left',
            'marginLeft': '10%'}),
        # Add explanatory text here using html.P
        html.P(
            'Boxplot showing when the frequency peaks (i.e. when the model was at the hight of popularity). Error bars showing first and most recent references.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='pop-dm-models-img', src='assets/pop_dm_models.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
# PLOT 5
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('5.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%'
        }),
        html.H3('Mass Range Coverage for Dark Matter Models', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left',
            'marginLeft': '10%'
            }),
        # Add explanatory text here using html.P
        html.P(
            'Plot of the mass range (in GeV) covered by the models. For macho´s and pbh I have added solar mass after their labels in parenthesis.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='mass-dm-models-img', src='assets/mass_dm_models.svg', style={'width': '100%', 'height': 'auto'}),
# PLOT 6
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('6.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%'
        }),
        html.H3("Categorized dark matter models", style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left',
            'marginLeft': '10%'
            }),
        # Add explanatory text here using html.P
        html.P(
            'Charts showing the proportions of models covered in the literature. Grouped by particles-based, exotic, supersymmetric, and interaction-based. Hover to see paper count for respective model',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left', 
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Div(dcc.Graph(id='sunburst-dm-models'), style={'display': 'flex', 'justifyContent': 'center'}),
        #html.Div(dcc.Graph(id='treemap-dm-models'), style={'display': 'flex', 'justifyContent': 'center'}),
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
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='stellar-objects-img', src='assets/top20_stellar_objects.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_11_layout():
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
def page_12_layout():
    return html.Div([
        html.H2('Citations vs. Downloads', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        
        html.P(
            'This page shows the scatter plot depicting the relationship between citations and downloads. Hover over points to view details such as title, first author, and publication year.',
            style={'fontFamily': 'DejaVu Sans Mono', 'color': dark_theme['text'], 'textAlign': 'center', 'padding': '5px', 'lineHeight': '1', 'fontSize': '12px', 'width': '80%', 'margin': '0 auto'}
        ),
        
        dcc.Graph(id='citations-downloads-scatter', figure=scatter_fig, style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_13_layout():
    return html.Div([
# PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('Authors', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'marginLeft': '10%'  # Optional: Align text with other elements
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('1.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%'  # Optional alignment for indentation
        }),
        html.H3('Top 20 most cited authors', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        html.P(
            'Plot of the 20 most cited authors in the data set (only first authors). ',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='top20-cited-authors-img', src='assets/author_citations.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
def page_14_layout():
    return html.Div([
        # PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('arXiv', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        
        html.H1('1.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%'
        }),
        
        html.H3('Metrics for arXiv representation', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        
        html.P(
            'Metric data based on a paper’s arXiv classification',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        
        # Center the images
        html.Img(id='metrics-vs-arXiv-img', src='assets/metrics_vs_arXiv_category.svg', style={
            'width': '80%', 
            'height': 'auto', 
            'margin': '0 auto',  # Centers image horizontally
            'display': 'block',  # Centers image within its block
            'marginBottom': '20px'
        }),
        
        html.Img(id='metrics-vs-arXiv_cat', src='assets/metrics_vs_arXiv_category.svg', style={
            'width': '80%', 
            'height': 'auto', 
            'margin': '0 auto',  # Centers image horizontally
            'display': 'block',  # Centers image within its block
            'marginBottom': '20px'
        }),
        
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_15_layout():
    return html.Div([
# PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('Keyword', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'marginLeft': '10%'  # Optional: Align text with other elements
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('1.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%'  # Optional alignment for indentation
        }),
        html.H3('Keyword by citations', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        html.P(
            'Top 20 keywords based on citations',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '1',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Img(id='keyword-vs-citations-img', src='assets/keyword_vs_citations.svg', style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}),
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
    elif pathname == '/page-11':
        return page_10_layout()
    elif pathname == '/page-12':
        return page_12_layout()
    elif pathname == '/page-13':
        return page_13_layout()
    elif pathname == '/page-14':
        return page_14_layout()
    elif pathname == '/page-15':
        return page_15_layout()
    elif pathname == '/about':
        return page_about_layout()


    else:
        return html.Div([
            html.H1("404 - Page Not Found", style={'textAlign': 'center', 'color': 'red'}),
            html.P("The page you are looking for does not exist.", style={'textAlign': 'center'}),
        ])

# Updated callback to only return the sunburst plot
@app.callback(
    Output('sunburst-dm-models', 'figure'),  # Only Sunburst output
    Input('url', 'pathname')
)
def update_plots(pathname):
    # Sunburst plot (static)
    fig_sunburst = px.sunburst(
        paper_counts, path=['dm_category', 'dm_models'], values='paper_count',
        color_discrete_sequence=spektrum_2
    )
    fig_sunburst.update_layout(
        font=dict(family="DejaVu Sans Mono", color=dark_theme['text']),
        plot_bgcolor=dark_theme['background'],
        paper_bgcolor=dark_theme['background'],
        margin=dict(t=50, l=25, r=25, b=25)
    )

    return fig_sunburst


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8054))
    app.run_server(debug=False, host='0.0.0.0', port=port)
