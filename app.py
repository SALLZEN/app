#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os
import requests
import random
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
#                                                                                          -> PLOT <-
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
    width=1000,
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

# most cited titles by arXiv
top_titles = df.nlargest(50, 'citations')
flat_data = top_titles.explode(['arxiv_category', 'citations']).reset_index(drop=True)

# Replace None or NaN in 'arxiv_category' with a placeholder
flat_data['arxiv_category'] = flat_data['arxiv_category'].fillna('Unknown')

# Create a combined column for the title and citations for easier labeling
flat_data['title_citation'] = flat_data['title'] + " (" + flat_data['citations'].astype(str) + " citations)"

# Sunburst plot where each arxiv_category has an outer ring of individual titles
fig_3 = px.sunburst(
    flat_data,
    path=['arxiv_category', 'title_citation'],
    values='citations',
    #title="Top 50 Most Cited Titles Grouped by arxiv_category",
    color='arxiv_category',  # Color by category for easy distinction
    color_discrete_sequence=px.colors.qualitative.Pastel  # Soft color palette for clarity
)

# Customize layout with larger size and styling
fig_3.update_layout(
    font=dict(
        family="DejaVu Sans Mono",  # Custom font
        size=14,  # Larger font size for readability
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=20,  # Larger title font
        color='#fff8e8',  # Title color
    ),
    plot_bgcolor='#20272d',  # Background color
    paper_bgcolor='#20272d',  # Outer background color
    margin=dict(t=60, l=10, r=10, b=10),  # Adjusting margins
    width=700,  # Increased width
    height=700,  # Increased height
    hoverlabel=dict(  # Hover label customization
        font=dict(family="DejaVu Sans Mono"),
        bgcolor='#333333',
        font_color='#fff8e8'
    )
)
# Update hovertemplate to show both citation count and percentage
fig_3.update_traces(
    hovertemplate="<b>%{label}</b><br>Citations: %{value}<br>Percentage: %{percentParent:.2%}",
)


# CITATIONS VS DOWNLOADS
# Create the bubble plot using Plotly
fig_4 = px.scatter(
    df,
    x='citations_normalized',
    y='downloads',
    size='citations',  # Size of the bubbles based on downloads
    hover_data=['title', 'first_author', 'year'],  # Hover info for papers
    #title='Top Cited Papers vs. Downloads',
    labels={'citations_normalized': 'Normalized Citations', 'downloads': 'Downloads'},
    opacity=0.7,  # Slight transparency for better overlapping visibility
    size_max=40,  # Maximum bubble size
)

# Customize layout
fig_4.update_layout(
    font=dict(
        family="DejaVu Sans Mono",  # Custom font
        size=12,
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=18,
        color='#fff8e8',  # Title color
    ),
    plot_bgcolor='#20272d',  # Background color
    paper_bgcolor='#20272d',  # Outer background
    width=1000,  # Custom width
    height=600,  # Custom height
    xaxis=dict(
        title_font=dict(color='#fff8e8'),  # X-axis label color
        tickfont=dict(color='#fff8e8'),  # X-axis tick label color
        gridcolor='rgba(255, 255, 255, 0.2)',  # Grid color
        linecolor='rgba(255, 255, 255, 0.5)',  # Axis line color
        type='log'
    ),
    yaxis=dict(
        title_font=dict(color='#fff8e8'),  # Y-axis label color
        tickfont=dict(color='#fff8e8'),  # Y-axis tick label color
        gridcolor='rgba(255, 255, 255, 0.2)',  # Grid color
        linecolor='rgba(255, 255, 255, 0.5)',  # Axis line color
        type='log',
    ),
    hoverlabel=dict(
        bgcolor='#333333',  # Background color for hover labels
        font_size=12,  # Font size for hover labels
        font_family="DejaVu Sans Mono",  # Hover font
        font_color='#FFF8E8'  # Text color for hover labels
    )
)

# Customize marker styling (bubbles)
fig_4.update_traces(
    marker=dict(
        color='#F2A604',  # Custom color for bubbles
        line=dict(
            width=0.5,
            color='#20272d'  # Border color around bubbles
        )
    )
)


# theoretical vs experimental
# Filter data for years after 1980
df_filtered = df[df['year'] > 1980]

# Ensure that `bibcode` is included in the filtered DataFrame
theoretical_vs_experimental_df = df_filtered[['year', 'particles', 'gravity', 'detectors', 'colliders', 'stellar_objects', 'methods', 'inferences', 'telescopes', 'dm_models', 'bibcode']].copy()

# Define research focus based on non-null values, same as before
theoretical_vs_experimental_df['category'] = None
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['particles'].notnull(), 'category'] = 'Particles'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['gravity'].notnull(), 'category'] = 'Gravity'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['detectors'].notnull(), 'category'] = 'Detectors'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['colliders'].notnull(), 'category'] = 'Colliders'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['stellar_objects'].notnull(), 'category'] = 'Stellar Objects'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['methods'].notnull(), 'category'] = 'Methods'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['inferences'].notnull(), 'category'] = 'Inferences'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['telescopes'].notnull(), 'category'] = 'Telescopes'
theoretical_vs_experimental_df.loc[theoretical_vs_experimental_df['dm_models'].notnull(), 'category'] = 'Dark matter models'

# Drop rows without a category
theoretical_vs_experimental_df = theoretical_vs_experimental_df.dropna(subset=['category'])

# Map categories to "Theoretical" or "Experimental"
theoretical_map = {
    'Particles': 'Experimental', 'Detectors': 'Experimental', 'Colliders': 'Experimental', 'Telescopes': 'Experimental',
    'Gravity': 'Theoretical', 'Dark matter models': 'Theoretical', 'Stellar Objects': 'Theoretical', 'Methods': 'Theoretical', 'Inferences': 'Theoretical'
}
theoretical_vs_experimental_df['research_type'] = theoretical_vs_experimental_df['category'].map(theoretical_map)

# Group by year, category, and research type, counting unique bibcodes
grouped_data = theoretical_vs_experimental_df.groupby(['year', 'category', 'research_type'])['bibcode'].nunique().reset_index(name='counts')


# Separate the data for experimental and theoretical subplots
experimental_data = grouped_data[grouped_data['research_type'] == 'Experimental']
theoretical_data = grouped_data[grouped_data['research_type'] == 'Theoretical']

# Define color palettes
experimental_colors = ['#AED3D4', '#65D4CC', '#5E9E95', '#A4D4AC']
theoretical_colors = ['#ECD305', '#FCC405', '#F2A604', '#DC8334', '#EC5B1D']

# Create subplot
fig_5 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Experimental Research", "Theoretical Research"),
    shared_yaxes=True
)

# Add experimental bars
for i, category in enumerate(experimental_data['category'].unique()):
    subset = experimental_data[experimental_data['category'] == category]
    fig_5.add_trace(
        go.Bar(
            x=subset['year'],
            y=subset['counts'],
            name=category,
            marker_color=experimental_colors[i % len(experimental_colors)]
        ),
        row=1, col=1
    )

# Add theoretical bars
for i, category in enumerate(theoretical_data['category'].unique()):
    subset = theoretical_data[theoretical_data['category'] == category]
    fig_5.add_trace(
        go.Bar(
            x=subset['year'],
            y=subset['counts'],
            name=category,
            marker_color=theoretical_colors[i % len(theoretical_colors)]
        ),
        row=1, col=2
    )

# Update layout
fig_5.update_layout(
    font=dict(
        family="DejaVu Sans Mono",
        size=12,
        color='#fff8e8'
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=18,
        color='#fff8e8'
    ),
    plot_bgcolor='#20272d',
    paper_bgcolor='#20272d',
    width=1000,
    height=600,
    yaxis_type="linear",
    yaxis2_type='linear',
    xaxis=dict(
        title="Year",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    xaxis2=dict(
        title="Year",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    yaxis=dict(
        title="Papers",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    yaxis2=dict(
        title="Papers",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    ),
    barmode='stack'
)

#FIG 6
import numpy as np
df_b = df[df['year'] > 1933]
research_data = df_b[['year', 'theory', 'particles', 'gravity', 'detectors', 'colliders', 'dm_models', 'telescopes', 'stellar_objects', 'methods', 'inferences', 'citations']].copy()

research_data['research_focus'] = None

research_data.loc[research_data['theory'].notnull(), 'research_focus'] = 'Theories'
research_data.loc[research_data['particles'].notnull(), 'research_focus'] = 'Particles'
research_data.loc[research_data['gravity'].notnull(), 'research_focus'] = 'Gravitational phenomena'
research_data.loc[research_data['detectors'].notnull(), 'research_focus'] = 'Detectors'
research_data.loc[research_data['colliders'].notnull(), 'research_focus'] = 'Colliders'
research_data.loc[research_data['stellar_objects'].notnull(), 'research_focus'] = 'Stellar Objects'
research_data.loc[research_data['methods'].notnull(), 'research_focus'] = 'Methods'
research_data.loc[research_data['inferences'].notnull(), 'research_focus'] = 'Inferences'
research_data.loc[research_data['telescopes'].notnull(), 'research_focus'] = 'Telescopes'
research_data.loc[research_data['dm_models'].notnull(), 'research_focus'] = 'Dark Matter Models'

research_data = research_data.dropna(subset=['research_focus'])

grouped_citation_data = research_data.groupby(['year', 'research_focus'])['citations'].sum().unstack(fill_value=0)

grouped_citation_data_log = np.log10(grouped_citation_data + 1)  

fig_6 = px.imshow(
    grouped_citation_data_log.T, 
    aspect='auto',
    labels=dict(x="Year", y="Research Focus", color="Citations"),
    color_continuous_scale='electric',
)

fig_6.update_layout(
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    ),
    font=dict(
        family="DejaVu Sans Mono", 
        size=12,
        color='#fff8e8',  
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=18,
        color='#fff8e8',  
    ),
    plot_bgcolor='#20272d',  
    paper_bgcolor='#20272d',  
    width=1000,  
    height=600, 
)

fig_6.update_traces(
    hovertemplate='Year: %{x}<br>Research Focus: %{y}<br>Citations: %{customdata}<extra></extra>',
    customdata=grouped_citation_data.T.values  
)

tickvals_log = np.log10([1, 10, 100, 1000, 10000, 100000])  
ticktext_normal = ['1', '10', '100', '1k', '10k', '100k'] 

fig_6.update_coloraxes(
    colorbar_tickvals=tickvals_log,  
    colorbar_ticktext=ticktext_normal  
)


# PLOT 7
df_filtered_2 = df[df['year'] > 1980]

# Ensure that `bibcode` and `citations` are included in the filtered DataFrame
theoretical_vs_experimental_df_2 = df_filtered_2[['year', 'particles', 'gravity', 'detectors', 'colliders', 'stellar_objects', 'methods', 'inferences', 'telescopes', 'dm_models', 'bibcode', 'citations']].copy()

# Define research focus based on non-null values
theoretical_vs_experimental_df_2['category'] = None
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['particles'].notnull(), 'category'] = 'Particles'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['gravity'].notnull(), 'category'] = 'Gravity'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['detectors'].notnull(), 'category'] = 'Detectors'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['colliders'].notnull(), 'category'] = 'Colliders'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['stellar_objects'].notnull(), 'category'] = 'Stellar Objects'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['methods'].notnull(), 'category'] = 'Methods'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['inferences'].notnull(), 'category'] = 'Inferences'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['telescopes'].notnull(), 'category'] = 'Telescopes'
theoretical_vs_experimental_df_2.loc[theoretical_vs_experimental_df_2['dm_models'].notnull(), 'category'] = 'Dark Matter Models'

# Drop rows without a category
theoretical_vs_experimental_df_2 = theoretical_vs_experimental_df_2.dropna(subset=['category'])

# Map categories to "Theoretical" or "Experimental"
theoretical_map_2 = {
    'Particles': 'Experimental', 'Detectors': 'Experimental', 'Colliders': 'Experimental', 'Telescopes': 'Experimental',
    'Gravity': 'Theoretical', 'Dark Matter Models': 'Theoretical', 'Stellar Objects': 'Theoretical', 'Methods': 'Theoretical', 'Inferences': 'Theoretical'
}
theoretical_vs_experimental_df_2['research_type'] = theoretical_vs_experimental_df_2['category'].map(theoretical_map_2)

# Group by year, category, and research type, summing citations
grouped_data_2 = theoretical_vs_experimental_df_2.groupby(['year', 'category', 'research_type'])['citations'].sum().reset_index(name='total_citations')

# Separate the data for experimental and theoretical subplots
experimental_data_2 = grouped_data_2[grouped_data_2['research_type'] == 'Experimental']
theoretical_data_2 = grouped_data_2[grouped_data_2['research_type'] == 'Theoretical']

# Define color palettes
experimental_colors_2 = ['#AED3D4', '#65D4CC', '#5E9E95', '#A4D4AC']
theoretical_colors_2 = ['#ECD305', '#FCC405', '#F2A604', '#DC8334', '#EC5B1D']

# Create subplot
fig_7 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Experimental Research", "Theoretical Research"),
    shared_yaxes=True
)

# Add experimental bars
for i, category in enumerate(experimental_data_2['category'].unique()):
    subset = experimental_data_2[experimental_data_2['category'] == category]
    fig_7.add_trace(
        go.Bar(
            x=subset['year'],
            y=subset['total_citations'],  # Use citation totals
            name=category,
            marker_color=experimental_colors_2[i % len(experimental_colors_2)]
        ),
        row=1, col=1
    )

# Add theoretical bars
for i, category in enumerate(theoretical_data_2['category'].unique()):
    subset = theoretical_data_2[theoretical_data_2['category'] == category]
    fig_7.add_trace(
        go.Bar(
            x=subset['year'],
            y=subset['total_citations'],  # Use citation totals
            name=category,
            marker_color=theoretical_colors_2[i % len(theoretical_colors_2)]
        ),
        row=1, col=2
    )

# Update layout with citation labels
fig_7.update_layout(
    font=dict(
        family="DejaVu Sans Mono",
        size=12,
        color='#fff8e8'
    ),
    title_font=dict(
        family="DejaVu Sans Mono",
        size=18,
        color='#fff8e8'
    ),
    plot_bgcolor='#20272d',
    paper_bgcolor='#20272d',
    width=1000,
    height=600,
    yaxis_type="linear",
    yaxis2_type='linear',
    xaxis=dict(
        title="Year",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    xaxis2=dict(
        title="Year",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    yaxis=dict(
        title="Total Citations",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    yaxis2=dict(
        title="Total Citations",
        title_font=dict(color='#fff8e8'),
        tickfont=dict(color='#fff8e8'),
        gridcolor='rgba(255, 255, 255, 0.2)',
        linecolor='rgba(255, 255, 255, 0.5)',
        griddash="dash",
        showline=False,
    ),
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    ),
    barmode='stack'
)


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
                {'label': 'Dark Matter Models', 'value': '/dmm'},
                {'label': 'co occurrence graphs', 'value': '/co_occurrence'},
                {'label': 'Metrics', 'value': '/metrics'},
                {'label': 'Authors', 'value': '/authors'},
                {'label': 'arXiv', 'value': '/arXiv'},
                {'label': 'Keywords', 'value': '/keywords'},
                {'label': 'Research focus', 'value': '/research_focus'},
                {'label': 'Particles', 'value': '/particles'},
                {'label': 'Gravity', 'value': '/gravity'},
                {'label': 'Theories', 'value': '/theories'},
                {'label': 'Telescopes', 'value': '/telescopes'},
                {'label': 'Detectors', 'value': '/detectors'},
                {'label': 'Colliders', 'value': '/colliders'},
                {'label': 'Inferences', 'value': '/inferences'},
                {'label': 'Methods', 'value': '/methods'},
                {'label': 'Stellar objects', 'value': '/stellar_objects'},
                {'label': 'Mass range', 'value': '/mass_range'},
            ],
            value='/dmm',  # Default value
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
    html.H4("dark matter research data", id='header-title', style={'textAlign': 'center', 'color': dark_theme['text']}),
    style={'backgroundColor': dark_theme['background'], 'padding': '10px'}
)

# Page layouts without light/dark mode switching
def page_dmm_layout():
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
    'marginLeft': '10%',
    'marginTop': '2%',
    'marginBottom': '2%' 
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
        html.Div(
            dcc.Graph(id='barplot-dm-models', figure=fig_1, style={'width': '80%', 'height': 'auto', 'marginBottom': '20px'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),

# PLOT 2
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(
            id='top20-dm-models-img',
            src='assets/top20_dm_models_grid.svg',
            style={
                'width': '80%', 
                'height': 'auto', 
                'display': 'block',  # Centers image within its block
                'margin': '0 auto'   # Centers image horizontally
            }),
# PLOT 3
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('3.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(
            id='citations-dm-models-img',
            src='assets/dm_models_vs_citations.svg',
            style={
                'width': '80%', 
                'height': 'auto', 
                'display': 'block',  # Centers image within its block
                'margin': '0 auto'   # Centers image horizontally
            }),
        
#PLOT 4
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('4.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(
            id='pop-dm-models-img',
            src='assets/pop_dm_models.svg',
            style={
                'width': '80%', 
                'height': 'auto', 
                'display': 'block',  # Centers image within its block
                'margin': '0 auto'   # Centers image horizontally
            }),
# PLOT 5
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('5.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(
            id='mass-dm-models-img',
            src='assets/mass_dm_models.svg',
            style={
                'width': '80%', 
                'height': 'auto', 
                'display': 'block',  # Centers image within its block
                'margin': '0 auto'   # Centers image horizontally
            }),
# PLOT 6
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('6.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(dcc.Graph(id='sunburst-dm-models'), style={'display': 'flex', 'justifyContent': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_particles_layout():
    return html.Div([
        html.H2('Particles', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='particles-img', src='assets/top_20_particles_grid_dark.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_gravity_layout():
    return html.Div([
        html.H2('Gravitational phenomena', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='gravity-img', src='assets/top15_gravity_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='gravity-all-img', src='assets/all_gravity_terms_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_theories_layout():
    return html.Div([
        html.H2('Theories', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='theory-img', src='assets/top20_theory_grid_dark.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_telescopes_layout():
    return html.Div([
        html.H2('Telescopes', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='telescopes-img', src='assets/top20_telescopes_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_detectors_layout():
    return html.Div([
        html.H2('Detectors', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='detector-img', src='assets/top20_detectors_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_colliders_layout():
    return html.Div([
        html.H2('Colliders', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='colliders-img', src='assets/top20_colliders_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_inferences_layout():
    return html.Div([
        html.H2('Inferences', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='inferences-img', src='assets/top20_inferences_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_methods_layout():
    return html.Div([
        html.H2('Methods', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='methods-img', src='assets/top20_methods_grid.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_stellar_objects_layout():
    return html.Div([
        html.H2('Mass range', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H3('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'center'}),
        html.Img(id='stellar-objects-img', src='assets/top20_stellar_objects.svg', style={'width': '100%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_mass_range_layout():
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
def page_metrics_layout():
    return html.Div([
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('Metrics', style={
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
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Citations vs. Downloads', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),        
        html.P(
            'This page shows the scatter plot depicting the relationship between citations and downloads. Hover over points to view details such as title, first author, and publication year.',
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
        html.Div(
            dcc.Graph(
                id='citations-downloads-scatter',
                figure=fig_4,
                style={
                    'width': '80%',      # Controls the container size of the graph
                    'height': 'auto', 
                    'marginBottom': '20px'
                }
            ),
            style={'display': 'flex', 'justifyContent': 'center'}  # Centers the graph on the page
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_authors_layout():
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
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top20-cited-authors-img', src='assets/author_citations.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
# PLOT 2
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Top 20 most active authors', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        html.P(
            'Plot of the top 20 most productive authors (in terms of paper count). ',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top20-productive-authors-img', src='assets/author_paper_count.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),



        
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
def page_arXiv_layout():
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
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        # Center the images
        html.Img(id='metrics-vs-arXiv-class-img', src='assets/metrics_vs_arXiv_classification.svg', style={
            'width': '80%', 
            'height': 'auto', 
            'margin': '0 auto', 
            'display': 'block', 
            'marginBottom': '20px'
        }),
        
        html.Img(id='metrics-vs-arXiv_cat', src='assets/metrics_vs_arXiv_category.svg', style={
            'width': '80%', 
            'height': 'auto', 
            'margin': '0 auto',  # Centers image horizontally
            'display': 'block',  # Centers image within its block
            'marginBottom': '20px'
        }),
# PLOT 3
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('top titles by arXiv category', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        
        html.P(
            'Interactive plot of the most cited papers grouped by their arXiv category. Click to select slices; hover for details on titles and citations.',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='titles-arXiv-fig', figure=fig_3, style={'width': '50%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_keywords_layout():
    return html.Div([
# PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('Keywords', style={
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
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='keyword-vs-citations-img', src='assets/keyword_vs_citations.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Keyword = "Dark Matter"', style={
            'fontFamily': 'DejaVu Sans Mono',
            'fontWeight': '400',
            'color': dark_theme['text'],
            'textAlign': 'left', 
            'marginLeft': '10%'  
        }),
        html.P(
            'The following series of plots are made from a filtered subset of the data, specifically the subset of papers which have the explicit keyword "dark matter". For breivity, I will refer to this subset as "Dark Matter Research."',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='papercount-img', src='assets/dm_papers_over_time.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='citations-img', src='assets/total_citations_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='reads-img', src='assets/total_reads_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='downloads-img', src='assets/total_downloads_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='arxiv-distribution-img', src='assets/arxiv_distribution_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='citations-models-darkmatter-img', src='assets/dm_models_citations_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='particles-stellar-objects-darkmatter-img', src='assets/top_stellar_objects_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top-models-darkmatter-img', src='assets/top_models_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top-models-citations-darkmatter-img', src='assets/dm_models_and_citations_over_time_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top-models-downloads-darkmatter-img', src='assets/dm_models_and_downloads_over_time_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top-models-reads-darkmatter-img', src='assets/dm_models_and_reads_over_time_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_research_focus_layout():
    return html.Div([
        # local header
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('Research focus', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),        
        
# PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('1.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Theoretical vs. Experimental | paper count', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        
        html.P(
            'Approximate estimation of research focus between experimental and theoretical efforts based on paper count.',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='theoretical-experimental-papers-fig', figure=fig_5, style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),

# PLOT 2
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('2.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Theoretical vs. Experimental | citations', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        
        html.P(
            'Approximate estimation of research focus between experimental and theoretical efforts based on citations.',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='theoretical-experimental-citations-fig', figure=fig_7, style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
# PLOT 3
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.H1('3.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('citations by research focus', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        
        html.P(
            'Citations by research focus. hover for details.',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='citations-research-focus-fig', figure=fig_6, style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),




        
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_co_occurrence_layout():
    return html.Div([
         html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

         html.H2('Co occurrence graphs', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
         }),        
        
# PLOT 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
         
        html.H1('1.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H3('Network graph of co-occurrences between dark matter models, particles, and theories.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),
        
        html.P(
            'This network plot displays the co-occurrences between dark matter models, theories, and particles. The size of the node is proportional to the number of co-occurrences. Navigate by click and drag, select any node by clicking to view its connections.',
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
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        # Embed the HTML file in an Iframe
        html.Div(
            html.Iframe(
                src="assets/network/index.html",  # Load from assets directory
                style={
                    "width": "1200px",   # Adjust as needed
                    "height": "750px", # Match the network height
                    "border": "none",
                    "display": "block",
                    "margin": "0 auto"
                }
            ),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the Iframe
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
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
    if pathname == '/dmm':
        return page_dmm_layout()
    elif pathname == '/particles':
        return page_particles_layout()
    elif pathname == '/gravity':
        return page_gravity_layout()
    elif pathname == '/theories':
        return page_theories_layout()
    elif pathname == '/telescopes':
        return page_telescopes_layout()
    elif pathname == '/detectors':
        return page_detectors_layout()
    elif pathname == '/colliders':
        return page_colliders_layout()
    elif pathname == '/inferences':
        return page_inferences_layout()
    elif pathname == '/methods':
        return page_methods_layout()
    elif pathname == '/stellar_objects':
        return page_stellar_objects_layout()
    elif pathname == '/mass_range':
        return page_mass_range_layout()
    elif pathname == '/metrics':
        return page_metrics_layout()
    elif pathname == '/authors':
        return page_authors_layout()
    elif pathname == '/arXiv':
        return page_arXiv_layout()
    elif pathname == '/keywords':
        return page_keywords_layout()
    elif pathname == '/research_focus':
        return page_research_focus_layout()
    elif pathname == '/co_occurrence':
        return page_co_occurrence_layout()
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
