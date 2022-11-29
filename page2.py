import pandas as pd

import plotly.express as px
import plotly.offline as py 
import plotly.graph_objects as go

import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from app import app

import base64

df_raison = pd.read_excel('Résultats OpinionWay _ LaborIA.xlsx', sheet_name = 'Raisons')
df_frein = pd.read_excel('Résultats OpinionWay _ LaborIA.xlsx', sheet_name = 'Freins')
df_impact = pd.read_excel('Résultats OpinionWay _ LaborIA.xlsx', sheet_name = 'Effets')

df_raison['Pourcentage'] = df_raison['Pourcentage'] * 100
df_raison['Pourcentage'] = round(df_raison['Pourcentage'])
df_raison['Pourcentage'] = df_raison['Pourcentage'].astype(int)

df_frein['Pourcentage'] = df_frein['Pourcentage'] * 100
df_frein['Pourcentage'] = round(df_frein['Pourcentage'])
df_frein['Pourcentage'] = df_frein['Pourcentage'].astype(int)

df_impact['Pourcentage'] = df_impact['Pourcentage'] * 100
df_impact['Pourcentage'] = round(df_impact['Pourcentage'])
df_impact['Pourcentage'] = df_impact['Pourcentage'].astype(int)

df_raison2 = df_raison.groupby(['Theme', 'Detail']).sum()
df_raison2.reset_index()
df_raison = df_raison2.merge(df_raison, on = ['Theme', 'Detail'])

df_raison['Norm'] = df_raison['Pourcentage_y'] / df_raison['Pourcentage_x'] * 100

df_raison = df_raison.rename(columns = {'Pourcentage_y' : 'Pourcentages cumulés', 
                                        'Norm' : 'Valeurs normalisées'})
df_raison = df_raison.drop(columns = 'Pourcentage_x')

df_frein2 = df_frein.groupby(['Theme', 'Detail']).sum()
df_frein2.reset_index()
df_frein = df_frein2.merge(df_frein, on = ['Theme', 'Detail'])

df_frein['Norm'] = df_frein['Pourcentage_y'] / df_frein['Pourcentage_x'] * 100

df_frein = df_frein.rename(columns = {'Pourcentage_y' : 'Pourcentages cumulés', 
                                        'Norm' : 'Valeurs normalisées'})
df_frein = df_frein.drop(columns = 'Pourcentage_x')

df_impact2 = df_impact.groupby(['Theme', 'Detail']).sum()
df_impact2.reset_index()
df_impact = df_impact2.merge(df_impact, on = ['Theme', 'Detail'])

df_impact['Norm'] = df_impact['Pourcentage_y'] / df_impact['Pourcentage_x'] * 100

df_impact = df_impact.rename(columns = {'Pourcentage_y' : 'Pourcentages cumulés', 
                                        'Norm' : 'Valeurs normalisées'})
df_impact = df_impact.drop(columns = 'Pourcentage_x')

df_raison['Pourcentages cumulés'] = df_raison['Pourcentages cumulés'].astype(str) + '%'
df_frein['Pourcentages cumulés'] = df_frein['Pourcentages cumulés'].astype(str) + '%'
df_impact['Pourcentages cumulés'] = df_impact['Pourcentages cumulés'].astype(str) + '%'

#app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])

#image_filename = 'Logo_matrice2.png'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename2 = 'Logo_LaborIA.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

colors = {
    'background': '#0a3a44',
    'text': '#0a3a44'
}

dico_theme = {
    'Type de SIA' : 'Type de SIA',
    "Secteur d'activité" : "Secteur d'activité",
    'Service' : 'Service',
    "Taille d'entreprise" : "Taille d'entreprise"
}

layout = html.Div(style={
    #'backgroundColor': colors['background'],
    'backgroundColor' : 'white'
},
    children=[
        html.Div([
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image2.decode()), 
                style = {
                    'display': 'inline-block', 
                    'width' : '200px',
                    'height' : '66px', 
                    'marginTop' : '4px', 
                    'marginLeft' : '20px'}),
            html.H2(
                children="Utilisation des Systèmes d'Intelligence Artificielle\n en entreprise",
                style={
                    #'backgroundColor': colors['background'],
                    'backgroundColor': 'white',
                    'display': 'inline-block', 
#                    'width' : '74%',
                    'width' : '70%', 
                    'textAlign': 'center', 
                    'marginTop' : '50px',
                    'color': colors['text']
                })
#            html.Img(
#                src='data:image/png;base64,{}'.format(encoded_image.decode()), 
#                style = {
#                    'display': 'inline-block', 
#                    'width' : '120px', 
#                    'height' : '120px', 
#                    'marginTop' : '10px'})
        ]),
        html.Div([
            dcc.Dropdown(
                id='question',
                value = 'Raisons',
                options = ['Raisons', 'Freins', 'Impacts'],
                multi=False, 
                clearable=False)
        ], style={
#            'backgroundColor': colors['background'],
            'backgroundColor': 'white', 
            'width': '20%', 
            'display': 'inline-block', 
            'marginRight' : '20px', 
            'padding': '20px 5px', 
            'font-size' : '30'}
        ),
        html.Div([
            html.H5(
                children="En fonction de", 
                style={'color': colors['text']}
            ),
            dcc.RadioItems(
                id='theme', 
                value="Type de SIA",
                options=dico_theme,
                style={
#                    'backgroundColor': colors['background'],
                    'backgroundColor': 'white',
                    'color': colors['text']
                      },
                labelStyle={'display': 'inline-block', 'marginTop': '2px', 'marginLeft' : '20px'}
            )],
            style={'width': '60%', 'display': 'inline-block', 'padding': '50'}
        ),
        html.Div([
            dcc.Graph(
                id='barres',
                style={
 #                   'backgroundColor': colors['background'],
                    'backgroundColor': 'white',
                    'color': colors['text']
                }
            )
        ], style={
            'width': '100%', 
            'display': 'inline-block', 
            'padding': '0 20'}
        )
    ])

@app.callback(
    Output('barres', 'figure'),
    Input('question', 'value'),
    Input('theme', 'value')
    )
def update_fig(question, theme):
    if question == 'Raisons':
        df_theme = df_raison[df_raison['Theme'] == theme]
        df_theme = df_theme.sort_values(by = 'Detail')
        fig = px.bar(df_theme, 
                     y = 'Detail', 
                     x = 'Valeurs normalisées', 
                     color = 'Réponse', 
                     orientation = 'h', 
                     text = 'Pourcentages cumulés',
 #                    template = 'plotly_dark',
                     template = 'plotly_white', 
                     color_discrete_sequence=px.colors.qualitative.Antique)
        fig.update_layout(yaxis_title=None)
        fig.update_xaxes(visible=False)
        fig.update_layout(
            yaxis_tickfont_size=14,
            legend=dict(
                font_size = 14,
                title_font_size=16,
#                orientation="h",
#                yanchor="bottom",
#                y= -0.25,
#                xanchor="right",
#                x=-0.2
            ))
    elif question == 'Freins':
        df_theme = df_frein[df_frein['Theme'] == theme]
        df_theme = df_theme.sort_values(by = 'Detail')
        fig = px.bar(df_theme, 
                     y = 'Detail', 
                     x = 'Valeurs normalisées', 
                     color = 'Réponse', 
                     orientation = 'h', 
                     text = 'Pourcentages cumulés',
#                     template = 'plotly_dark',
                     template = 'plotly_white', 
                     color_discrete_sequence=px.colors.qualitative.Antique)
        fig.update_layout(yaxis_title=None)
        fig.update_xaxes(visible=False)
        fig.update_layout(
            yaxis_tickfont_size=14,
            legend=dict(
                font_size = 14,
                title_font_size=16, 
#                orientation="h",
#                yanchor="bottom",
#                y= -0.25,
#                xanchor="right"
#                x=-0.2
            ))
    else:
        df_theme = df_impact[df_impact['Theme'] == theme]
        df_theme = df_theme.sort_values(by = 'Detail')
        fig = px.bar(df_theme, 
                     y = 'Detail', 
                     x = 'Valeurs normalisées', 
                     color = 'Réponse', 
                     orientation = 'h', 
                     text = 'Pourcentages cumulés',
#                     template = 'plotly_dark',
                     template = 'plotly_white', 
                     color_discrete_sequence=px.colors.qualitative.Antique)
        fig.update_layout(yaxis_title=None)
        fig.update_xaxes(visible=False)
        fig.update_layout(
            yaxis_tickfont_size=14,
            legend=dict(
                font_size = 14,
                title_font_size=16,
#                orientation="h",
#                yanchor="bottom",
#                y= -0.25,
#                xanchor="right"
#                x=-0.2
            ))
    return fig

    