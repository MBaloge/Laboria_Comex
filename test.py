#!/usr/bin/python
# -*- coding: latin-1 -*-
from dash import  dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

import home
import page1
import page2

# building the navigation bar
# https://github.com/meredithwan/covid-dash-app
colors = {
    'background': '#B0C4DE',
    'text': '#00152F'}

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Consommation de Gaz", href="page1"),
        dbc.DropdownMenuItem("Import/Export de Gaz", href="page2")

    ],

    nav = True,
    in_navbar = True,
    label = "Explore",
    toggle_style={"color": "gold"},# pour mettre 'Explore' en gold ,
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src="/assets/virus.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("L\'Energie en Europe", className="ml-2",style={'color':"gold"})),
                    ],
                    align="center",
                    no_gutters=True,
                    
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            )
        ]
    ),
    color="darkblue",
    dark=True,
    className="mb-0" # ce parametre met la navbar coller à la page (mb-0) pour laisser une marge mb-3,5 ou jouer dans reset avec magin
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
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