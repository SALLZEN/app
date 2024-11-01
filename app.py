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
# Replace NaN or empty arxiv_category with a placeholder "No class"
df['arxiv_category'] = df['arxiv_category'].apply(lambda x: ', '.join(x) if isinstance(x, list) else (x if pd.notnull(x) else 'No class'))
df['arxiv_category'] = df['arxiv_category'].replace('', 'No class')  # Ensure empty strings are replaced with "No class"

# Group by 'year' and count the number of publications
publications_per_year = df.groupby('year').size().reset_index(name='publication_count')

# Create a DataFrame that includes the count and percentage of arxiv_category per year
arxiv_distribution = df.groupby(['year', 'arxiv_category']).size().reset_index(name='category_count')
arxiv_distribution = arxiv_distribution.merge(publications_per_year, on='year')
arxiv_distribution['percentage'] = (arxiv_distribution['category_count'] / arxiv_distribution['publication_count']) * 100

# Format arxiv_distribution for hover information
# Sort arxiv_distribution by 'category_count' in descending order
arxiv_distribution = arxiv_distribution.sort_values(by='category_count', ascending=False)

# Create the 'formatted_info' column with the sorted data
arxiv_distribution['formatted_info'] = arxiv_distribution.apply(
    lambda row: f"{row['arxiv_category']}: {row['category_count']} ({row['percentage']:.1f}%)<br>", axis=1
)

# Aggregate formatted_info by year
hover_data = arxiv_distribution.groupby('year')['formatted_info'].apply(lambda x: ''.join(x)).reset_index(name='arxiv_distribution')

# Create a DataFrame with titles for years with 15 or fewer papers
titles_per_year = df.groupby('year')['title'].apply(lambda x: '<br>'.join(x) if len(x) <= 15 else '').reset_index(name='titles')

# Merge all hover data
merged_df = publications_per_year.merge(hover_data, on='year', how='left').merge(titles_per_year, on='year', how='left')

# Create the Plotly figure
fig_X = go.Figure()

# Add a line trace for publications per year
fig_X.add_trace(go.Scatter(
    x=merged_df['year'],
    y=merged_df['publication_count'],
    mode='lines+markers',
    line=dict(color='#E09351', width=1),
    marker=dict(size=8),
    hovertemplate=(
        '<b>Year:</b> %{x}<br>' +
        '<b>Publications:</b> %{y}<br>' +
        '<b>arXiv Categories:</b><br>%{customdata[0]}' +
        '<br><b>Titles:</b><br>%{customdata[1]}<extra></extra>'
        if '%{customdata[1]}' != '' else  # Display titles conditionally
        '<b>Year:</b> %{x}<br>' +
        '<b>Publications:</b> %{y}<br>' +
        '<b>arXiv Categories:</b><br>%{customdata[0]}<extra></extra>'
    ),
    customdata=merged_df[['arxiv_distribution', 'titles']].values  # Pass both the arXiv distribution and titles
))

# Update the layout
fig_X.update_layout(
    font=dict(
        family="DejaVu Sans Mono",  # Custom font
        size=12,
    ),
    title_font=dict(
        family="DejaVu Sans Mono",  # Title font customization
        size=18,
        color='#fff8e8',  # Title color
    ),
    plot_bgcolor='#20272d',  # Custom background color
    paper_bgcolor='#20272d',  # Custom outer background color
    width=1000,  # Custom width
    height=600,  # Custom height
    xaxis=dict(
        title_font=dict(color='#fff8e8'),  # X-axis label color
        tickfont=dict(color='#fff8e8'),  # X-axis tick label color
        gridcolor='rgba(255, 255, 255, 0.2)',  # X-axis grid color (faint white)
        linecolor='rgba(255, 255, 255, 0.5)',  # X-axis line color
        type='linear'
    ),
    yaxis=dict(
        title_font=dict(color='#fff8e8'),  # Y-axis label color
        tickfont=dict(color='#fff8e8'),  # Y-axis tick label color
        gridcolor='rgba(255, 255, 255, 0.2)',  # Y-axis grid color (faint white)
        linecolor='rgba(255, 255, 255, 0.5)',  # Y-axis line color
        type='log',
    ),
    hoverlabel=dict(
        bgcolor='#333333',
        font_size=12,
        font_family="DejaVu Sans Mono",
        font_color='#FFF8E8'
    ),
    showlegend=False
)

#-> PLOT <-
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
        html.Hr(style={'border': '1px solid #E09351FF', 'width': '85%', 'margin': '10px auto', 'opacity': '0.7'}),
        dcc.Dropdown(
            id='page-selector-dropdown',
            options=[
                {'label': 'Dark Matter publications', 'value': '/papers'},
                {'label': 'Dark Matter Models', 'value': '/dmm'},
                {'label': 'Co-occurrence graphs', 'value': '/co_occurrence'},
                {'label': 'Co-occurrence matrix', 'value': '/matrix'},
                {'label': 'Citation network', 'value': '/citation_network'},
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
            value='/papers',  # Default value
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
    html.H4("DARK MATTER RESEARCH DATA", id='header-title', style={'textAlign': 'center', 'color': dark_theme['text']}),
    style={'backgroundColor': dark_theme['background'], 'padding': '10px'}
)

def page_dmm_layout():
    return html.Div([
# PLOT 1        
html.H1('DARK MATTER MODELS', style={
    'fontFamily': 'DejaVu Sans Mono', 
    'fontWeight': '400', 
    'color': dark_theme['text'], 
    'textAlign': 'left',  # Change to left justification
    'marginLeft': '10%'  # Optional: Align text with other elements
}),

html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
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

html.H2('Top 20 most frequently referenced dark matter models', style={
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
        'lineHeight': '2',
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
        html.H2('Top 20 most frequently referenced dark matter models', style={
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
                'lineHeight': '2',
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
        html.H2('Top 20 Dark Matter Models by Citations', style={
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
                'lineHeight': '2',
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
        html.H2('Prevalence of Dark Matter Models in Papers Over Time', style={
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
                'lineHeight': '2',
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
        html.H2('Mass Range Coverage for Dark Matter Models', style={
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
                'lineHeight': '2',
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
        html.H2("Categorized dark matter models", style={
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
                'lineHeight': '2',
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
        html.H1('PARTICLES', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.Img(id='particles-img', src='assets/top_20_particles_grid_dark.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_gravity_layout():
    return html.Div([
        html.H1('GRAVITATIONAL PHENOMENA', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='gravity-img', src='assets/top15_gravity_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='gravity-all-img', src='assets/all_gravity_terms_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_theories_layout():
    return html.Div([
        html.H1('THEORY', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='theory-img', src='assets/top20_theory_grid_dark.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_telescopes_layout():
    return html.Div([
        html.H1('TELESCOPES', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='telescopes-img', src='assets/top20_telescopes_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_detectors_layout():
    return html.Div([
        html.H1('DETECTORS', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='detector-img', src='assets/top20_detectors_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_colliders_layout():
    return html.Div([
        html.H1('COLLIDERS', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='colliders-img', src='assets/top20_colliders_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_inferences_layout():
    return html.Div([
        html.H1('INFERENCES', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='inferences-img', src='assets/top20_inferences_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_methods_layout():
    return html.Div([
        html.H1('METHODS', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='methods-img', src='assets/top20_methods_grid.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_stellar_objects_layout():
    return html.Div([
        html.H1('STELLAR OBJECTS', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Grid plot showing frequency of reference over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Img(id='stellar-objects-img', src='assets/top20_stellar_objects.svg', style={'width': '80%', 'height': 'auto'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_mass_range_layout():
    return html.Div([
        html.H1('MASS RANGE', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.H2('Use frequency of mass/energy expressions over time.', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Div(
            html.Img(id='mass-img', src='assets/mass_range.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
def page_metrics_layout():
    return html.Div([
        html.H1('METRICS', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'marginLeft': '10%'  # Optional: Align text with other elements
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
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
        html.H2('Citations vs. Downloads', style={
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
                'lineHeight': '2',
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
        html.H1('AUTHORS', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'marginLeft': '10%'  # Optional: Align text with other elements
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
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
        html.H2('Top 20 most cited authors', style={
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
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top20-cited-authors-img', src='assets/author_citations.svg', style={'width': '70%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
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
        html.H2('Top 20 most active authors', style={
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
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top20-productive-authors-img', src='assets/author_paper_count.svg', style={'width': '70%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),



        
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
def page_arXiv_layout():
    return html.Div([
# PLOT 1
            html.H1('ARXIV CLASSIFICATION', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        
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
        
        html.H2('Metrics for arXiv representation', style={
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
                'lineHeight': '2',
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
        html.H2('top titles by arXiv category', style={
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
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='titles-arXiv-fig', figure=fig_3, style={'width': '40%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})


def page_keywords_layout():
    return html.Div([
# PLOT 1
        html.H1('KEYWORDS', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',  # Change to left justification
            'marginLeft': '10%'  # Optional: Align text with other elements
        }),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
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
        html.H2('Keyword by citations', style={
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
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='keyword-vs-citations-img', src='assets/keyword_vs_citations.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
        
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
# PLOT 2
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
        html.H2('Keyword = "Dark Matter"', style={
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
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Img(id='top-authors-keyword-img', src='assets/top_authors_dm_keyword.svg', style={'width': '80%', 'height': 'auto', 'marginBottom': '20px', 'margin': '0 auto', 
            'display': 'block'}),
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
        html.H1('RESEARCH FOCUS', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
        }),        
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '16%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
# PLOT 1
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
        html.H2('Theoretical vs. Experimental | paper count', style={
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
                'lineHeight': '2',
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
        html.H2('Theoretical vs. Experimental | citations', style={
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
                'lineHeight': '2',
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
        html.H2('citations by research focus', style={
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
                'lineHeight': '2',
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
         html.H1('CO-OCCURRENCE GRAPHS', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%'
         }),        
        
# GRAPH 1
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
         
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
        html.H2('Co-occurrences between dark matter models, particles, and theories.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%',
            'lineHeight': '2',
        }),
        
        html.P(
            'This network graph displays the co-occurrences between dark matter models, theories, and particles. The size of the node is proportional to the number of co-occurrences. '
            'Navigate by click and drag, select any node by clicking to view its connections.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
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
                    "width": "1000px",   # Adjust as needed
                    "height": "750px", # Match the network height
                    "border": "none",
                    "display": "block",
                    "margin": "0 auto"
                }
            ),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the Iframe
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
# GRAPH 2   
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
        html.H2('Co-occurrences between dark matter models, particles, particle colliders, and detectors.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%',
            'lineHeight': '2',
            'width': '80%',
        }),
        
        html.P(
            'This network graph displays the co-occurrences between dark matter models, particles, particle colliders, and detectors.'
            'The size of the node is proportional to the number of co-occurrences. Navigate by click and drag, select any node by clicking to view its connections.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        # Embed the HTML file in an Iframe
        html.Div(
            html.Iframe(
                src="assets/network2/index.html",  # Load from assets directory
                style={
                    "width": "1000px",   # Adjust as needed
                    "height": "750px", # Match the network height
                    "border": "none",
                    "display": "block",
                    "margin": "0 auto"
                }
            ),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the Iframe
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
# GRAPH 3   
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
        html.H2('Co-occurrences between dark matter models, stellar objects, telescopes, and gravitational phenomena.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%',
            'lineHeight': '2',
            'width': '80%',
        }),
        
        html.P(
            'This network plot displays the co-occurrences between dark matter models, particles, particle colliders, and detectors.'
            'The size of the node is proportional to the number of co-occurrences. Navigate by click and drag, select any node by clicking to view its connections.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        # Embed the HTML file in an Iframe
        html.Div(
            html.Iframe(
                src="assets/network3/index.html",  # Load from assets directory
                style={
                    "width": "1000px",   # Adjust as needed
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
        html.H1('ABOUT THE PROJECT.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '32%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%',}),
        html.P([
            'This project was conceptualized within a larger project on the philosophy and history of dark matter. When writing a paper on the bibliographical history of dark matter, '
            'I realized that few or no sources overlooking the diversity of research which specialized on dark matter was available. While the ',
            html.A('Astrophysics Data System', href='https://ui.adsabs.harvard.edu/', target='_blank', style={'color': '#E09351FF', 'text-decoration': 'underline'}),
            ' (operated by the Smithsonian Astrophysical Observatory under NASA Cooperative Agreement) is an excellent data source with a broad coverage, using it to discern the '
            'larger historical picture, or the evolution of the dark matter hypothesis over time, was not optimal. Because of this, I decided to create my own bibliographical '
            'database, covering all the papers containing the phrase "dark matter" somewhere in the paper from the ADS. I did this by programmatically accessing the ADS servers using their API service, '
            'which allows the token-bearer to select search parameters, and which bibliographical fields to return (the below example script returns "bibcode, title, year, keyword_norm, abstract, page"):'
            ], style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Pre(
            """
            import time
            import json
            import requests
            from urllib.parse import urlencode
            from bs4 import BeautifulSoup

            def query_ads_api(encoded_query, rows=2000, start=0, token=''):
                data = []

                while True:
                    query_url = ("https://api.adsabs.harvard.edu/v1/search/query?{encoded_query}"
                                 "&rows={rows}"
                                 "&start={start}").format(encoded_query=encoded_query, rows=rows, start=start)

                    response = requests.get(query_url, headers={'Authorization': 'Bearer ' + token})

                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', 5))
                        print(f"Rate limit exceeded. Waiting for {retry_after} seconds before retrying.")
                        time.sleep(retry_after)
                        continue

                    response.raise_for_status()

                    try:
                        docs = response.json()['response']['docs']
                    except KeyError:
                        print('No docs found')
                        break

                    data.extend(docs)

                    start += rows
                    print(f"Processed {start} documents.")

                    if not docs:
                        break

                try:
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                except (TypeError, ValueError) as e:
                    print("Error writing JSON file:", e)

                return data
            # main executable
            def main():
                encoded_query = urlencode({"q": "full:\"dark matter\"",
                                           "fl": "bibcode, title, year, keyword_norm, abstract, page"})
                token = '<API_TOKEN>'
                results = query_ads_api(encoded_query, token=token)

                print(f"Total results: {len(results)}")

            if __name__ == "__main__":
                main()
                """,
            style={
            'backgroundColor': '#20272d',
            'color': '#E09351FF',
            'padding': '10px',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'fontFamily': 'DejaVu Sans Mono',
            'fontSize': '12px',
            'width': '60%',
            'marginLeft': '10%'
        }),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.P([
            'The above script was made to return a json of all natural language fields, and in conjunction with serveral other scripts '
            'the full specification of data fields for the 177.284 returning bibcodes are the following: bibcode, arxiv_class, database, doctype, '
            'first_author, keyword_norm, keyword_schema, title, year, read_count, citation_count, citation_count_norm, citation (references), page, '
            'abstract, data. Below is an example of the json structure for a single bibcode (not exhaustive): '
            ], style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Pre(
            """
            {
        "bibcode": "1994A&A...285...79P",
        "arxiv_class": [
            "astro-ph"
        ],
        "database": [
            "astronomy"
        ],
        "doctype": "article",
        "first_author": "Pfenniger, D.",
        "keyword_norm": [
            "cosmology dark matter",
            "galaxies kinematics and dynamics",
            "galaxies intergalactic medium",
            "galaxies evolution",
            "astrophysics"
        ],
        "keyword_schema": [
            "Astronomy",
            "Astronomy",
            "Astronomy",
            "Astronomy",
            "arXiv"
        ],
        "title": [
            "Is dark matter in spiral galaxies cold gas? I. Observational constraints and dynamical clues about galaxy evolution"
        ],
        "year": "1994",
        "read_count": 10,
        "data": [
            "SIMBAD:1"
        ],
        "citation_count": 333,
        "citation_count_norm": 111.0,
        "citation": [
            "2009arXiv0904.4638R",
            "2010A&A...512A..17B",
            "2010A&A...520A.107B",
            "2010AIPC.1241..154C",
            "2010AdAst2010E...1B",
            "2010ApJ...715.1497J",
            "2010ApPhB.101..321T",
            "2010PhDT.......243G",
            "2011A&A...525A.108H",
            "2011A&A...532A.121H",
            "2011ApJ...736...91L",
            "2011MNRAS.416.1936T",
            "2011MNRAS.417..198V",
            "2011Prama..76....1C",
            "2012A&A...537A..78B",
            "2012A&A...543L...6G",
            "2012A&A...544A..55B",
            "2012A&A...548A..52B",
            "2012AJ....143...40M",
            "2012ApJ...751...30M",
            "2012JPhCS.354a2004D",
            "2012MNRAS.420.3071S",
            "2012arXiv1204.4649D",
            "2013AstL...39..291Z",
            "2013LRR....16....6A",
            "2013MNRAS.429.1949A",
            "2013MNRAS.429.2537M",
            "2013MNRAS.434.2814W",
            "2014MNRAS.437.3072K",
            "2014MNRAS.443....2E",
            "2014SAAS...37....1B",
            "2015A&A...575A..32C",
            "2015A&A...578A..18F",
            "2015A&A...584A.113L",
            "2015ApJ...808..115M",
            "2015Galax...3..184L",
            "2015MNRAS.450.1032K",
            "2015MNRAS.451.2889K",
            "2015sf2a.conf..385I",
            "2016A&A...591A.100F",
            "2016MNRAS.457.3666C",
            "2017A&A...602A..45L",
            "2017CaJPh..95..156H",
            "2017IAUS..321..172M",
            "2017PhyU...60....3Z",
            "2018A&A...609A.131G",
            "2018A&A...613A..64F",
            "2018LRR....21....2A",
            "2019A&A...629A..87D",
            "2019ApJ...881...69W",
            "2019MNRAS.487.2148G",
            "2019PhRvD.100d3028Q",
            "2019Symm...11.1009J",
            "2020MNRAS.493.1736R",
            "2020arXiv201208326K",
            "2021MNRAS.502.3294W",
            "2021R&QE...63..643S",
            "2022ApJ...932....4W",
            "2022MNRAS.513.2491T",
            "2023ApJ...945....3S",
            "2023PASP..135j5002H",
            "2023PDU....4201339K",
            "2023Symm...15..160T",
            "2024MNRAS.527.2697S",
            "2024arXiv240400944B"
        ]
    },
                """,
            style={
            'backgroundColor': '#20272d',
            'color': '#E09351FF',
            'padding': '10px',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'fontFamily': 'DejaVu Sans Mono',
            'fontSize': '12px',
            'width': '80%',
            'marginLeft': '10%'
        }),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.P([
            'Through a series of programmatic operations, the data was cleaned, ordered, and fit for exploring the published history of dark matter research. '
            'Some operations are worth explaining further for transparency, since their results are hard to intuitively grasp otherwise.', html.Br(),
            html.Br(),
            'ARXIV CLASS', html.Br(),
            html.Br(),
            'Since a single bibcode can have several arxiv classes, I had to create a script that accounted for this. Otherwise, a simple operation like '
            'for example finding the most frequent arxiv class in dark matter research would be skewed. Fortunately, the list order of appearance in the ADS '
            'system is also the order of significance. This allowed me to pivot the "arxiv_class" column and attribute a relevance score for each classification '
            'associated with a bibcode. A simple geometric sequence [1, 0.5, 0.25, 0.125, ...] was mapped to the order of appearance of arxiv class, representing its '
            'relevance as a numerical weight. This script was written in "R":'
            ], style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Pre(
            """
            df_longer <- arxiv |> 
              unnest_longer(c('arxiv_class'), keep_empty = TRUE, values_to = NULL, 
                            indices_to = "arxiv_rank", indices_include = TRUE)

            # Filter out bibcodes with NA in arxiv_class
            df_with_arxiv <- df_longer |>
              filter(!is.na(arxiv_class))

            df_without_arxiv <- df_longer |>
              filter(is.na(arxiv_class))

            arxiv_01 <- df_with_arxiv |>
              pivot_wider(names_from = arxiv_rank, values_from = arxiv_class, 
                          names_prefix = "arxiv.ordinal.", names_repair = "unique")

            arxiv_02 <- arxiv_01 |>
              mutate(across(starts_with("arxiv.ordinal."), ~factor(.x, levels = unique(.x[!is.na(.x)]))))

            weight_factor <- function(rank) {
              1 / (2 ^ (rank - 1))
            }

            arxiv_03 <- arxiv_02 |>
              mutate(across(starts_with("arxiv.ordinal."), 
                            ~ ifelse(!is.na(.), weight_factor(as.numeric(str_extract(cur_column(), "\\d+$"))),
                                     NA_real_), .names = "weight_{col}"))

            # Pivot longer to get arxiv_classification and arxiv_relevance_score columns
            arxiv_03 <- arxiv_03 |>
              pivot_longer(c(starts_with("arxiv.ordinal.")), 
                           names_to = "arxiv_rank", 
                           values_to = "arxiv_classification", 
                           values_drop_na = TRUE) |>
              pivot_longer(c(starts_with("weight_arxiv.ordinal.")), 
                           names_to = "weight_rank", 
                           values_to = "arxiv_relevance_score", 
                           values_drop_na = TRUE) |>
              filter(str_extract(arxiv_rank, "\\d+$") == str_extract(weight_rank, "\\d+$")) |>
              select(-arxiv_rank, -weight_rank)

            # Add column for arXiv category
            arxiv_03 <- arxiv_03 |> 
              mutate(arxiv_category = case_when(
                grepl("^astro", arxiv_classification) ~ "astrophysics",
                grepl("^cond-mat", arxiv_classification) ~ "condensed matter",
                grepl("^hep-", arxiv_classification) ~ "high-energy physics",
                grepl("^math", arxiv_classification) ~ "mathematics",
                grepl("^cs", arxiv_classification) ~ "computer science",
                grepl("^quant-ph", arxiv_classification) ~ "quantum physics",
                grepl("^gr-qc", arxiv_classification) ~ "general relativity and quantum cosmology",
                grepl("^nucl-", arxiv_classification) ~ "nuclear physics",
                grepl("^physics", arxiv_classification) ~ "physics",
                grepl("^q-bio", arxiv_classification) ~ "quantitative biology",
                grepl("^q-fin", arxiv_classification) ~ "quantitative finance",
                grepl("^stat", arxiv_classification) ~ "statistics",
                grepl("^econ", arxiv_classification) ~ "economics",
                grepl("^eess", arxiv_classification) ~ "electrical engineering and systems science",
                grepl("^nlin", arxiv_classification) ~ "nonlinear sciences",
                TRUE ~ "Other"
              ))

            # Combine the parts
            arxiv_04 <- arxiv_03 |>
              bind_rows(df_without_arxiv |> 
                          mutate(arxiv_classification = NA, arxiv_relevance_score = NA))

            # Remove left over columns
            data <- arxiv_04 |> select(-c(arxiv_class, arxiv_rank))

            distinct(data)
                """,
            style={
            'backgroundColor': '#20272d',
            'color': '#E09351FF',
            'padding': '10px',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'fontFamily': 'DejaVu Sans Mono',
            'fontSize': '12px',
            'width': '60%',
            'marginLeft': '10%'
        }),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.P([
            'NATURAL LANGUAGE PROCESSING', html.Br(),
            html.Br(),
            'In order to gauge the ontological and epistemological trends and propositions for dark matter, it was important to extract relevant entities and '
            'terms from the text data. First, the abstracts were cleaned from any plain text HTML and LaTeX that were present in the abstracts, taking care to '
            'not accidentally remove any scientifically relevant notation. Then, a normalization function was created to homogenize any abbreviations or acronyms '
            'present, for example "wimp" and "weakly interacting massive particle". Ordinary stopword removal and lowercaseing was also done. Below, an example script '
            'of the extraction of terms related to dark matter models:'
            ], style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Pre(
            """
            import pandas as pd
            import re

            df = pd.read_csv("csv_data/prior_to_lemmatization.csv")
            entities = [
                {"label": "DARK MATTER MODELS", "pattern": "Self-Interacting Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "SIDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Warm Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "WDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Axion"},
                {"label": "DARK MATTER MODELS", "pattern": "Axions"},
                {"label": "DARK MATTER MODELS", "pattern": "ALP"},  
                {"label": "DARK MATTER MODELS", "pattern": "Axion-Like Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Axion-Like Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "Sterile Neutrino Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Sterile Neutrino"},
                {"label": "DARK MATTER MODELS", "pattern": "Fuzzy Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "FDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Supersymmetric Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Neutralino Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Neutralino"},
                {"label": "DARK MATTER MODELS", "pattern": "Kaluza-Klein Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Kaluza-Klein"},
                {"label": "DARK MATTER MODELS", "pattern": "WIMP"},  
                {"label": "DARK MATTER MODELS", "pattern": "WIMPS"},
                {"label": "DARK MATTER MODELS", "pattern": "Weakly Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Weakly-Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Weakly Interacting Massive Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "Weakly-Interacting Massive Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "Gravitino Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Gravitino"},
                {"label": "DARK MATTER MODELS", "pattern": "Tachyon Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Tachyon"},
                {"label": "DARK MATTER MODELS", "pattern": "Scalar Field Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "SFDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Vector Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "VDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Primordial Black Holes"},
                {"label": "DARK MATTER MODELS", "pattern": "Primordial Black Hole"},
                {"label": "DARK MATTER MODELS", "pattern": "PBH"},
                {"label": "DARK MATTER MODELS", "pattern": "Superfluid Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "SFD"},
                {"label": "DARK MATTER MODELS", "pattern": "Quintessence Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Quintessence"},
                {"label": "DARK MATTER MODELS", "pattern": "QDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Ultralight Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "ULDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Non-thermal Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Mirror Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Macroscopic Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "MACDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Asymmetric Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "ADM"},
                {"label": "DARK MATTER MODELS", "pattern": "Composite Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Leptophilic Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Bosonic Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "BDM"},
                {"label": "DARK MATTER MODELS", "pattern": "Anapole Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "WIMPzilla"}, 
                {"label": "DARK MATTER MODELS", "pattern": "Self-Annihilating Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "MaCHOs"}, 
                {"label": "DARK MATTER MODELS", "pattern": "Massive Compact Halo Object"}, 
                {"label": "DARK MATTER MODELS", "pattern": "Super Weakly Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Super Weakly Interacting Massive Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "SWIMP"},
                {"label": "DARK MATTER MODELS", "pattern": "SWIMPS"},
                {"label": "DARK MATTER MODELS", "pattern": "Massive Compact Halo Objects"},  
                {"label": "DARK MATTER MODELS", "pattern": "Fermionic Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Little Higgs"},  
                {"label": "DARK MATTER MODELS", "pattern": "QCD Axions"},  
                {"label": "DARK MATTER MODELS", "pattern": "Quantum Chromodynamics Axions"},
                {"label": "DARK MATTER MODELS", "pattern": "Emergent Gravity"}, 
                {"label": "DARK MATTER MODELS", "pattern": "Glueball"},
                {"label": "DARK MATTER MODELS", "pattern": "Glueball Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Strongly Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Strongly Interacting Massive Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "SIMP"},
                {"label": "DARK MATTER MODELS", "pattern": "SIMPS"},
                {"label": "DARK MATTER MODELS", "pattern": "Elastically Decoupling Relic"},
                {"label": "DARK MATTER MODELS", "pattern": "ELDER DM"},
                {"label": "DARK MATTER MODELS", "pattern": "Feebly Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "Feebly Interacting Massive Particle"},
                {"label": "DARK MATTER MODELS", "pattern": "FIMP"},
                {"label": "DARK MATTER MODELS", "pattern": "FIMPS"},
                {"label": "DARK MATTER MODELS", "pattern": "Decaying Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Dark Photon"},
                {"label": "DARK MATTER MODELS", "pattern": "Planckian Interacting Massive Particles"},
                {"label": "DARK MATTER MODELS", "pattern": "PIMP"},
                {"label": "DARK MATTER MODELS", "pattern": "Sterile Neutrino Dark Matter (Dodelson-Widrow)"},
                {"label": "DARK MATTER MODELS", "pattern": "Dodelson-Widrow Sterile Neutrino"},
                {"label": "DARK MATTER MODELS", "pattern": "WIMP-less Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "WIMP-less DM"},
                {"label": "DARK MATTER MODELS", "pattern": "Composite Asymmetric Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Composite ADM"},
                {"label": "DARK MATTER MODELS", "pattern": "Self-Interacting Dark Energy"},
                {"label": "DARK MATTER MODELS", "pattern": "SIDEN"},
                {"label": "DARK MATTER MODELS", "pattern": "Hidden-Sector Dark Matter"},
                {"label": "DARK MATTER MODELS", "pattern": "Hidden-Sector DM"}
            ]

            entity_patterns = '|'.join([r'\b' + re.escape(entity["pattern"]) + r'\b' for entity in entities])

            entity_regex = re.compile(entity_patterns, re.IGNORECASE)

            def extract_entities(text):
                if isinstance(text, str):
                    return list(set(entity_regex.findall(text))) 
                else:
                    return []  

            df['dm_models'] = df['abstract_clean'].apply(extract_entities)
            print(df['dm_models'].head(10))
            -------------------------------
            0                                                   []
            1                                                   []
            2    [weakly interacting massive particle, weakly i...
            3    [axions, wimps, weakly interacting massive par...
            4                                                   []
            5                                                   []
            6                                                   []
            7                                                   []
            8    [neutralino dark matter, weakly-interacting ma...
            9                       [self-interacting dark matter]
            Name: dm_models, dtype: object

                """,
            style={
            'backgroundColor': '#20272d',
            'color': '#E09351FF',
            'padding': '10px',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'fontFamily': 'DejaVu Sans Mono',
            'fontSize': '12px',
            'width': '60%',
            'marginLeft': '10%'
        }),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
                html.P([
            'I created similar scripts for various relevant terms and entities [as seen in the plots] and joined the datasets by the bibcode key, ensuring '
            'consistency and completeness. The above scripts and descriptions are just a small sample of the total process of data extraction, manipulation, '
            'subsetting, and so on. Please contact me for further information or requests of subsets / ideas. Currently, I am building a machine learning model '
            'trained on the data that I hope will result in an AI model which users can chat with directly, answering any questions about the bibliographical history of dark matter.'
            ], style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_citation_network_layout():
    return html.Div([ 
        html.H1('CITATION NETWORK.', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'fontSize': '3em',
            'marginLeft': '10%',
            'marginTop': '2%',
            'marginBottom': '2%'
        }),
        html.H2('', style={
            'fontFamily': 'DejaVu Sans Mono', 
            'fontWeight': '400', 
            'color': dark_theme['text'], 
            'textAlign': 'left',
            'marginLeft': '10%',
            'lineHeight': '2',
            'width': '80%',
        }),
        
        html.P(
            'Citation network for papers with "dark matter" as keyword. Nodes are papers, links citations. Colors are given by arXiv classification, node size by number of citations. '
            'Navigate by click and drag, select any paper by clicking to view its connections, arXiv classification, year of publication, metric data, et.c. Most papers reference papers '
            'from their own arXiv classification, implying a low grade of interdisciplinarity.',
            style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        # Embed the HTML file in an Iframe
        html.Div(
            html.Iframe(
                src="assets/network4/index.html",  # Load from assets directory
                style={
                    "width": "1000px",   # Adjust as needed
                    "height": "750px", # Match the network height
                    "border": "none",
                    "display": "block",
                    "margin": "0 auto",
                    "fontFamily": "DejaVu Sans Mono",
                }
            ),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the Iframe
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})

def page_matrix_layout():
    return html.Div([
        html.H1('MATRIX PLOTS', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '40%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.P('Heatmap matrix plots showing co-occurrences between dark matter models and theoretical / experimental / methodological concepts.',
                style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_theories', src='assets/co_occurrence_dm_models_and_theories.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_particles', src='assets/co_occurrence_dm_models_and_particles.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_detectors', src='assets/co_occurrence_dm_models_and_detectors.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_colliders', src='assets/co_occurrence_dm_models_and_colliders.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_telescopes', src='assets/co_occurrence_dm_models_and_telescopes.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_inferences', src='assets/co_occurrence_dm_models_and_inferences.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_methods', src='assets/co_occurrence_dm_models_and_methods.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            html.Img(id='co_occurrence_dm_models_and_gravity', src='assets/co_occurrence_dm_models_and_gravity.svg', style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}  # Center the image
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
def page_papers_layout():
    return html.Div([
        html.H1('History of Dark Matter Publishing', style={'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': dark_theme['text'], 'textAlign': 'left', 'marginLeft': '10%'}),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '50%', 'margin': '10px 0', 'opacity': '0.5', 'marginLeft': '10%'}),
        html.P('All publications that contain the phrase "dark matter" somewhere in the text. Hover for additional information. '
               'If the sum of yearly publications <=15, paper titles are shown. For later papers, the distribution of arxiv classifications are shown. ',
                style={
                'fontFamily': 'DejaVu Sans Mono',
                'color': dark_theme['text'], 
                'textAlign': 'left',
                'marginLeft': '10%',
                'padding': '5px', 
                'lineHeight': '2',
                'fontSize': '12px',
                'width': '80%',  
                'margin': '0 auto',
            }
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
        html.Div(
            dcc.Graph(id='all-papers-img', figure=fig_X, style={'width': '80%', 'height': 'auto'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': dark_theme['background']})
# Main layout
app.layout = html.Div(id='main-div', style={'fontFamily': 'DejaVu Sans Mono', 'backgroundColor': dark_theme['background']}, children=[
    dcc.Location(id='url', refresh=False),  # Track the URL for page routing
    header,
    sidebar,
    html.Div(id='page-content',
             style={'marginTop': '80px', 'padding': '20px', 'backgroundColor': dark_theme['background']}),  # Dynamic content area
    html.Footer(
            "© 2024 Simon Allzén | s.allzen[at]uva.nl",  # Footer text
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
    elif pathname == '/papers':
        return page_papers_layout()
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
    elif pathname == '/citation_network':
        return page_citation_network_layout()
    elif pathname == '/matrix':
        return page_matrix_layout()
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

    
