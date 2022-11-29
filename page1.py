import pandas as pd

import plotly.express as px
import plotly.offline as py 
import plotly.graph_objects as go

import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import base64

import json

from app import app

df_SIA = pd.read_excel('Résultats OpinionWay _ LaborIA.xlsx', sheet_name = 'SIA')

df_SIA[df_SIA.columns[2::]] = df_SIA[df_SIA.columns[2::]] * 100
df_SIA[df_SIA.columns[2::]] = round(df_SIA[df_SIA.columns[2::]])
df_SIA[df_SIA.columns[2::]] = df_SIA[df_SIA.columns[2::]].astype(int)

for col in df_SIA.columns[2::]:
    df_SIA[col + ' (%)']= df_SIA[col].astype(str) + '%'

df_theme = df_SIA.loc[df_SIA['Theme'] == 'Ensemble', df_SIA.columns[2:9]].T.reset_index()
df_theme['pourcent'] = df_theme[15].astype(str) + '%'

df_taille = df_SIA[df_SIA['Theme'] == "Taille d'entreprise"]
df_secteur = df_SIA[df_SIA['Theme'] == "Secteur d'activité"]
df_service = df_SIA[df_SIA['Theme'] == "Service"]

liste_SIA = list(df_SIA.columns[2:9])
dico_color = {}
for i in range(len(liste_SIA)):
    dico_color[liste_SIA[i]] = px.colors.qualitative.Antique[i]

#app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])

#image_filename = 'Logo_matrice.png'
#image_filename = 'Logo_matrice2.png'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename2 = 'Logo_LaborIA.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

colors = {
    'background': '#0a3a44',
    'text': '#0a3a44'
}

fig1 = px.bar(df_theme,
             y = 'index', 
             x = 15, 
             orientation = 'h', 
             text = 'pourcent',
#             template = 'plotly_dark',
              template = 'plotly_white',
             color = 'index',
             color_discrete_sequence=px.colors.qualitative.Antique)
fig1.update_layout(yaxis_title = None, 
                  showlegend=False)
fig1.update_xaxes(visible=False)

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
                children="Types de Systèmes d'Intelligence Artificielle\n utilisés en entreprise",
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
            html.H4(
                children="Linguistique",
                id = 'type-SIA',
                style={
                    #'backgroundColor': colors['background'],
                    'backgroundColor': 'white',
                    'display': 'inline-block', 
                    'width' : '100%', 
                    'textAlign': 'center',
                    'color': colors['text']
                })
        ]),
        html.Div([
            dcc.Graph(
                id = 'SIA',
                figure = fig1,
                style={
#                    'backgroundColor': colors['background'], 
                    'backgroundColor' : 'white',
                    'height' : '300px', 
                    'color': colors['text']
                }
            )
        ], style={
            'width': '65%', 
            'display': 'inline-block', 
            'padding': '0 20'}
        ),
        html.Div([
            dcc.Graph(
                id = 'taille',
                style={
 #                   'backgroundColor': colors['background'], 
                    'backgroundColor' : 'white',
                    'height' : '250px',
                    'marginTop' : '50px',
                    'color': colors['text']
                }
            )
        ], style={
            'width': '35%', 
            'display': 'inline-block', 
            'padding': '0 20'}
        ),
        html.Div([
            dcc.Graph(
                id = 'secteur',
                style={
#                    'backgroundColor': colors['background'], 
                    'backgroundColor': 'white',
                    'height' : '250px', 
                    'color': colors['text']
                }
            )
        ], style={
            'width': '50%', 
            'display': 'inline-block', 
            'padding': '0 20'}
        ),
        html.Div([
            dcc.Graph(
                id = 'service',
                style={
#                    'backgroundColor': colors['background'], 
                    'backgroundColor' : 'white',
                    'height' : '250px', 
                    'color': colors['text']
                }
            )
        ], style={
            'width': '50%', 
            'display': 'inline-block', 
            'padding': '0 20'}
        ),
    ])        


@app.callback(
    Output('type-SIA', 'children'),
    Input('SIA', 'clickData'))
def update(clickData):
    if clickData != None:
        if clickData['points'][0]['label'] != 'Autre':
            text = clickData['points'][0]['label']
        elif clickData['points'][0]['label'] == 'Autre':
            text = 'Linguistique'
    else: 
        text = 'Linguistique'
    return text

@app.callback(
    Output('taille', 'figure'),
    Input('SIA', 'clickData')
    )
def update(clickData):
    df_taille = df_SIA[df_SIA['Theme'] == "Taille d'entreprise"]
    if clickData != None:
        if clickData['points'][0]['label'] != 'Autre':
            col = clickData['points'][0]['label']
            fig2 = px.bar(df_taille,
                         x = 'Detail', 
                         y = col, 
            #             orientation = 'h', 
                         text = col + ' (%)',
#                         template = 'plotly_dark',
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color[col]])
            fig2.update_layout(xaxis_title = None)
            fig2.update_yaxes(visible=False)
            fig2.update_xaxes(showline=True, linecolor='black')
        elif clickData['points'][0]['label'] == 'Autre':
            fig2 = px.bar(df_taille,
                         x = 'Detail', 
                         y = 'Linguistique', 
            #             orientation = 'h', 
                         text = 'Linguistique (%)',
#                         template = 'plotly_dark',
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color['Linguistique']])
            fig2.update_layout(xaxis_title = None)
            fig2.update_yaxes(visible=False) 
            fig2.update_xaxes(showline=True, linecolor='black')
    else:
        fig2 = px.bar(df_taille,
                     x = 'Detail', 
                     y = 'Linguistique', 
        #             orientation = 'h', 
                     text = 'Linguistique (%)',
#                     template = 'plotly_dark',
                      template = 'plotly_white',
                     color_discrete_sequence=[dico_color['Linguistique']])
        fig2.update_layout(xaxis_title = None)
        fig2.update_yaxes(visible=False)
        fig2.update_xaxes(showline=True, linecolor='black')
    return fig2


@app.callback(
    Output('secteur', 'figure'),
    Input('SIA', 'clickData')
    )
def update(clickData):
    df_secteur = df_SIA[df_SIA['Theme'] == "Secteur d'activité"]
    if clickData != None:
        if clickData['points'][0]['label'] != 'Autre':
            col = clickData['points'][0]['label']
            fig3 = px.bar(df_secteur,
                         x = 'Detail', 
                         y = col, 
            #             orientation = 'h', 
                         text = col + ' (%)',
#                         template = 'plotly_dark',
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color[col]])
            fig3.update_layout(xaxis_title = None)
            fig3.update_yaxes(visible=False)
            fig3.update_xaxes(showline=True, linecolor='black')
        elif clickData['points'][0]['label'] == 'Autre':
            fig3 = px.bar(df_secteur,
                         x = 'Detail', 
                         y = 'Linguistique', 
            #             orientation = 'h', 
                         text = 'Linguistique (%)',
#                         template = 'plotly_dark', 
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color['Linguistique']])
            fig3.update_layout(xaxis_title = None)
            fig3.update_yaxes(visible=False)
            fig3.update_xaxes(showline=True, linecolor='black')
    else:
        fig3 = px.bar(df_secteur,
                     x = 'Detail', 
                     y = 'Linguistique', 
        #             orientation = 'h', 
                     text = 'Linguistique (%)',
#                     template = 'plotly_dark',
                      template = 'plotly_white',
                     color_discrete_sequence=[dico_color['Linguistique']])
        fig3.update_layout(xaxis_title = None)
        fig3.update_yaxes(visible=False)
        fig3.update_xaxes(showline=True, linecolor='black')
    return fig3

@app.callback(
    Output('service', 'figure'),
    Input('SIA', 'clickData')
    )
def update(clickData):
    df_service = df_SIA[df_SIA['Theme'] == "Service"]
    if clickData != None:
        if clickData['points'][0]['label'] != 'Autre':
            col = clickData['points'][0]['label']
            fig4 = px.bar(df_service,
                         x = 'Detail', 
                         y = col, 
            #             orientation = 'h', 
                         text = col + ' (%)',
#                         template = 'plotly_dark',
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color[col]])
            fig4.update_layout(xaxis_title = None)
            fig4.update_yaxes(visible=False)
            fig4.update_xaxes(showline=True, linecolor='black')
        elif clickData['points'][0]['label'] == 'Autre':
            fig4 = px.bar(df_service,
                         x = 'Detail', 
                         y = 'Linguistique', 
            #             orientation = 'h', 
                         text = 'Linguistique (%)',
#                         template = 'plotly_dark',
                          template = 'plotly_white',
                         color_discrete_sequence=[dico_color['Linguistique']])
            fig4.update_layout(xaxis_title = None)
            fig4.update_yaxes(visible=False)
            fig4.update_xaxes(showline=True, linecolor='black')
    else:
        fig4 = px.bar(df_service,
                     x = 'Detail', 
                     y = 'Linguistique', 
        #             orientation = 'h', 
                     text = 'Linguistique (%)',
#                     template = 'plotly_dark',
                      template = 'plotly_white',
                     color_discrete_sequence=[dico_color['Linguistique']])
        fig4.update_layout(xaxis_title = None)
        fig4.update_yaxes(visible=False)
        fig4.update_xaxes(showline=True, linecolor='black')
    return fig4