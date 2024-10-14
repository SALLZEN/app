#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html, Input, Output
import dash_daq as daq  # Importing dash_daq for ToggleSwitch
import plotly.express as px
import pandas as pd
import os
df_unique = pd.read_csv('assets/df_unique.csv')
paper_counts = pd.read_csv('assets/paper_counts.csv')

spektrum = ['#F2A604', '#ED90AE', '#59A689', '#5DAA53', '#0A4E6B', '#232323']

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

server = app.server

light_sequential = ['#e09351', '#e4a671', '#e7b890', '#ebcbb0', '#efded0', '#f2f0ef']
dark_sequential = ['#292523', '#4e3b2c', '#725135', '#97673f', '#bb7d48', '#e09351']

# Define a custom color palette
darkmode = ['#20272D', '#2C3639', '#40534C', '#677D6A', '#D6BD98', '#FFEACF']
lightmode = ['#FFF8E8', '#FFEACF','#EDC775FF', '#E09351FF', '#1A3636', '#20272D']

# Use the palette for the dark theme
dark_theme = {
    'background': "#20272D",  # Darkest color for the background
    'text': darkmode[5],  # Lightest color for the text
    'secondary_text': darkmode[4],  # For secondary text (optional)
    'highlight': darkmode[3],  # For highlighted elements (optional)
}
light_theme = {
    'background': lightmode[0],  # lightest color for the background
    'text': lightmode[5],  # Darkest color for the text
    'secondary_text': lightmode[2],  # For secondary text (optional)
    'highlight': lightmode[3],  # For highlighted elements (optional)
}


# Sidebar Layout (static layout)
sidebar = html.Div(
    [
        html.H4("DaMaDi", id='sidebar-title', style={'align': 'center', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400'}),
        html.Hr(style={
            'border': '1px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.7'}),
        html.P("plots & graphs:", id='plots-text', style={'textAlign': 'center', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400'}),
        dcc.Dropdown(
            id='page-selector-dropdown',
            options=[
                {'label': 'static', 'value': '/page-1'},
                {'label': 'interactive', 'value': '/page-2'},
            ],
            value='/page-2',  # default value
            className='custom-dropdown',
        ),
        html.Hr(style={
            'border': '1px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.7'}),
        # Light/Dark Mode Toggle
        html.P("mode:", id='theme-text', style={'margin': '20px auto', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400'}),
        daq.ToggleSwitch(
            id='theme-toggle-switch',
            value=True,  # Default is light theme (False)
            color='#EDC775FF',  # Color of the switch
            style={'marginBottom': '15px'}
        ),
        html.Label("light", id='light-mode-label', style={'marginRight': '30px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'marginLeft': '10px'}),
        html.Label("dark", id='dark-mode-label', style={'marginRight': '110px', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'marginLeft': '15px'}),
        html.Hr(style={
            'border': '1px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.7'}),
    ],
    id='sidebar',  # Adding an ID to match the custom CSS
    style={'width': '15%', 'position': 'fixed', 'height': '100%'}
)
# Header with sticky style applied in custom_styles.css
header = html.Div(
    html.H1("d a r k . m a t t e r . r e s e a r c h . d a t a", id='header-title')
)

def page_1_layout(theme):
    return html.Div([
        html.Hr(style={
            'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('top 20 dark matter models (paper count)', style={
            'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text'], 'textAlign': 'center'}),

        # Dynamic Image for top 20 DM models
        html.Img(
            id='top20-dm-models-img',  # Unique ID
            src='assets/top20_dm_models_grid.svg',  # Default source (dark mode)
            style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('prevalence of dark matter models in papers over time', style={
            'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text'], 'textAlign': 'center'}),

        # Dynamic Image for prevalence of dark matter models
        html.Img(
            id='pop-dm-models-img',  # Unique ID for this image
            src='/assets/pop_dm_models.svg',  # Default source (dark mode)
            style={'width': '100%', 'height': 'auto', 'marginBottom': '20px'}
        ),

        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '80%', 'margin': '10px auto', 'opacity': '0.5'}),

        html.H2('mass range coverage for dark matter models', style={
            'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text'], 'textAlign': 'center'}),

        # Dynamic Image for mass range coverage of dark matter models
        html.Img(
            id='mass-dm-models-img',  # Unique ID for this image
            src='/assets/mass_dm_models.svg',  # Default source (dark mode)
            style={'width': '100%', 'height': 'auto'}
        ),
    ], style={'marginLeft': '18%', 'padding': '20px', 'backgroundColor': theme['background']})


def page_2_layout(theme):
    return html.Div([
        html.H2("Interactive Plots: Dark Matter Models", style={
            'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text'], 'textAlign': 'center'}),

        # Center the Sunburst plot (dynamic plot with ID)
        html.Div(
            dcc.Graph(id='sunburst-dm-models'),  # Use ID for the sunburst plot
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),

        # Center the Treemap plot (dynamic plot with ID)
        html.Div(
            dcc.Graph(id='treemap-dm-models'),  # Use ID for the treemap plot
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
        html.Hr(style={'border': '0.5px solid #E09351FF', 'width': '70%', 'margin': '10px auto', 'opacity': '0.5'}),
    ], style={'maxWidth': '1600px', 'margin': '0 auto', 'padding': '20px', 'backgroundColor': theme['background']})


app.layout = html.Div(id='main-div', style={'fontFamily': 'DejaVu Sans Mono'}, children=[
    dcc.Location(id='url', refresh=False),  # Track the URL for page routing
    header,
    sidebar,  # Static sidebar
    html.Div(id='page-content', style={'marginTop': '80px'}),  # Dynamic content area
])

@app.callback(
    Output('url', 'pathname'),  # Update the URL based on dropdown selection
    Input('page-selector-dropdown', 'value')  # Listen for dropdown value change
)
def update_url_from_dropdown(selected_page):
    return selected_page


@app.callback(
    [Output('page-content', 'children'),
     Output('main-div', 'style'),
     Output('header-title', 'style'),
     Output('sidebar', 'style'),
     Output('sidebar-title', 'style'),
     Output('plots-text', 'style'),
     Output('theme-text', 'style'),
     Output('page-selector-dropdown', 'style'),
     Output('light-mode-label', 'style'),
     Output('dark-mode-label', 'style')],
    [Input('url', 'pathname'),  # URL change (page routing)
     Input('theme-toggle-switch', 'value')]  # Theme change
)
def display_page(pathname, is_dark_mode):
    # Apply the selected theme
    theme = dark_theme if is_dark_mode else light_theme

    # Switch between pages based on the URL pathname
    if pathname == '/page-1':
        page_layout = page_1_layout(theme)
    elif pathname == '/page-2':
        page_layout = page_2_layout(theme)
    else:
        # Default to page 1 layout if no specific path is given
        page_layout = page_1_layout(theme)

    return [
        page_layout,
        {'backgroundColor': theme['background'], 'color': theme['text'], 'fontFamily': 'DejaVu Sans Mono'},  # main-div
        {'textAlign': 'center', 'color': theme['text'], 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400',
         'backgroundColor': theme['background']},  # header-title with background color
        {'width': '15%', 'position': 'fixed', 'height': '90%', 'backgroundColor': theme['background']},  # sidebar
        {'marginLeft': '20px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # sidebar-title
        {'marginLeft': '30px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # plots-text
        {'marginLeft': '30px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # theme-text
        {'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'backgroundColor': theme['background'],
         'color': theme['text']},  # dropdown styling
        {'marginLeft': '30px', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # light-mode label
        {'marginLeft': '100px', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # dark-mode-label
    ]

@app.callback(
    [Output('sunburst-dm-models', 'figure'),  # Sunburst plot update
     Output('treemap-dm-models', 'figure')],  # Treemap plot update
    Input('theme-toggle-switch', 'value')  # Theme toggle switch input
)
def update_plots(is_dark_mode):

    # Set common plot properties (adjustable based on theme)
    if is_dark_mode:
        bg_color = "#20272d"
        text_color = "#ffeacf"
        hover_bgcolor = "#20272d"
        hover_text_color = "#ffeacf"
    else:
        bg_color = "#FFF8E8"
        text_color = "#232323"
        hover_bgcolor = "#FFF8E8"
        hover_text_color = "#232323"

    # Sunburst plot (dynamic)
    fig_sunburst = px.sunburst(
        paper_counts,
        path=['dm_category', 'dm_models'],
        values='paper_count',
        color_discrete_sequence=spektrum,  # Assuming spektrum is defined
    )
    fig_sunburst.update_layout(
        font=dict(family="DejaVu Sans Mono", color=text_color),
        margin=dict(t=50, l=25, r=25, b=25),
        width=550, height=550,
        title_font_size=18,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        hoverlabel=dict(
            bgcolor=hover_bgcolor, font_size=14, font_family="DejaVu Sans Mono", font_color=hover_text_color
        ),
    )
    fig_sunburst.update_traces(
        textinfo="label+percent entry",
        insidetextorientation="radial",
        textfont=dict(size=14, color=text_color)
    )

    # Treemap plot (dynamic)
    fig_treemap = px.treemap(
        paper_counts,
        path=['dm_category', 'dm_models'],
        values='paper_count',
        color='paper_count',
        color_continuous_scale='ylgn',
    )
    fig_treemap.update_layout(
        font=dict(family="DejaVu Sans Mono", color=text_color),
        margin=dict(t=50, l=25, r=25, b=25),
        width=800, height=500,
        title_font_size=18,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        hoverlabel=dict(
            bgcolor=hover_bgcolor, font_size=14, font_family="DejaVu Sans Mono", font_color=hover_text_color
        ),
    )

    # Return both figures for the Sunburst and Treemap plots
    return fig_sunburst, fig_treemap



def display_page(pathname, is_dark_mode):
    # Apply the selected theme
    theme = dark_theme if is_dark_mode else light_theme

    # Switch between pages based on the URL pathname
    if pathname == '/page-1':
        page_layout = page_1_layout(theme)
    elif pathname == '/page-2':
        page_layout = page_2_layout(theme)
    else:
        # Default to page 1 layout if no specific path is given
        page_layout = page_1_layout(theme)

    return [
        page_layout,
        {'backgroundColor': theme['background'], 'color': theme['text'], 'fontFamily': 'DejaVu Sans Mono'},  # main-div
        {'textAlign': 'center', 'color': theme['text'], 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400',
         'backgroundColor': theme['background']},  # header-title with background color
        {'width': '15%', 'position': 'fixed', 'height': '90%', 'backgroundColor': theme['background']},  # sidebar
        {'marginLeft': '20px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # sidebar-title
        {'marginLeft': '30px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # plots-text
        {'marginLeft': '30px','fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # theme-text
        {'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'backgroundColor': theme['background'],
         'color': theme['text']},  # dropdown styling
        {'marginLeft': '30px', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # light-mode label
        {'marginLeft': '100px', 'fontFamily': 'DejaVu Sans Mono', 'fontWeight': '400', 'color': theme['text']},  # dark-mode-label
    ]

# Callback to update the image source when the theme is toggled
@app.callback(
    [Output('top20-dm-models-img', 'src'),  # Update the 'src' of top 20 DM models image
     Output('pop-dm-models-img', 'src'),    # Update the 'src' of prevalence of DM models image
     Output('mass-dm-models-img', 'src')],  # Update the 'src' of mass range coverage image
    Input('theme-toggle-switch', 'value')  # Listen for changes in the theme toggle
)
def update_image_sources(is_dark_mode):
    # Define file paths for dark and light mode
    if is_dark_mode:
        top20_src = 'assets/top20_dm_models_grid.svg'
        pop_src = 'assets/pop_dm_models.svg'
        mass_src = 'assets/mass_dm_models.svg'
    else:
        top20_src = 'assets/top20_dm_models_grid_light.svg'
        pop_src = 'assets/pop_dm_models_light.svg'
        mass_src = 'assets/mass_dm_models_light.svg'

    # Return updated sources for each image
    return top20_src, pop_src, mass_src


if __name__ == '__main__':
    # Get the PORT environment variable or default to 8050 if running locally
    port = int(os.environ.get('PORT', 8052))
    # Run the app on host 0.0.0.0 and the specified port
    app.run_server(debug=False, host='0.0.0.0', port=port)

