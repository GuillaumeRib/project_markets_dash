####################################
# IMPORTS
####################################
import pandas as pd
import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from pages import get_data
from pages import data_viz

####################################
# INIT APP
####################################
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}],
                use_pages=True
                )
server=app.server


####################################
# SELECT TEMPLATE for the APP
####################################
# loads the template and sets it as the default
load_figure_template("lux")


####################################
# Main Page layout
####################################

title = html.H1(children="US Markets Dashboard",
                className=('text-center mt-4'),
                style={'fontSize':36})

app.layout = html.Div(children=[
        dbc.Row(title),
        dbc.Row([html.Div(id='button',
                          children=[dbc.Button(page['name'],href=page['path'])
                                    for page in dash.page_registry.values()
                                ],
                      className=('text-center mt-4 mb-4'),style={'fontSize':20})
                 ]),
        # Content page
        dbc.Spinner(
            dash.page_container,
            fullscreen=True,
            show_initially=True,
            delay_hide=600,
            type='border',
            spinner_style={"width": "3rem", "height": "3rem"})

        ])

#############################################################################

####################################
# RUN the app
####################################
if __name__ == '__main__':
    server=app.server
    app.run_server(debug=True)
