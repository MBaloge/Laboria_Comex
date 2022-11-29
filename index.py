#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
import dash
from dash import  dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
import home
import page1
import page2
# https://github.com/meredithwan/covid-dash-app

colors = {
    'background': '#0a3a44'
#    'text': '#00152F'
    }

import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Accueil", href="home")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Description panel utilisant des SIA", href="page1"),
                dbc.DropdownMenuItem("Utilisateurs de SIA : raisons, freins, impacts", href="page2"),
            ],
            nav=True,
            in_navbar=True,
            label="Resultats",
            align_end=True
        ),
    ],
#    brand="NavbarSimple",
#    brand_href="#",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=False)