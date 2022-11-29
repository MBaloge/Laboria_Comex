#!/usr/bin/python
# -*- coding: latin-1 -*-
from dash import dcc 
from dash import html
import dash_bootstrap_components as dbc
import base64

colors = {
    'background': '#0a3a44'
#    'text': '#00152F'
    }
image_filename = 'Image_Home3.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div(style={
    'backgroundColor': colors['background'],
#    'backgroundColor' : 'white'
},
    children=[
        html.Div([
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'display': 'inline-block', 'width' : '1150px','height' : '630px',
                'marginLeft' : '150px'})]),      
    ])
