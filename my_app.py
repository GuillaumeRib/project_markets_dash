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
                external_stylesheets=[dbc.themes.YETI, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}],
                use_pages=True
                )
server=app.server


####################################
# SELECT TEMPLATE for the APP
####################################
# loads the template and sets it as the default
load_figure_template("yeti")


####################################
# Main Page layout
####################################

title = html.H1(children="US Markets Dashboard",
                className=('text-center mt-4'))

app.layout = html.Div(
    [
        dbc.Row(title),
        dbc.Row([html.Div(id='button',children=
            [dbc.Button(page['name'],href=page['path'])
            for page in dash.page_registry.values()
            ],
            className=('text-center mt-4 mb-4'),style={'fontSize':20})]),
        # Content page
        dash.page_container
        ])

##### Callback not properly setup, but avoid bug with animated chart ... ####
@app.callback(
    Output('graph', 'figure'),
    [Input('button', 'n_clicks')]
)
def update_chart(n_clicks):
    pass
    #fig = dcc.Graph(id='graph',figure=data_viz.line_yield_curve(df))
#############################################################################

####################################
# RUN the app
####################################
if __name__ == '__main__':
    server=app.server
    app.run_server(debug=True)
