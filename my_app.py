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

from us_rates import get_data
from us_rates import data_viz


####################################
# Load data & dfs
####################################
df = get_data.get_rates()


####################################
# INIT APP
####################################
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}]
                )
server=app.server



####################################
# SELECT TEMPLATE for the APP
####################################
# loads the template and sets it as the default
load_figure_template("yeti")


####################################
# FILL Template layout
####################################

title = html.H1(children="US Treasury Yield Curve",
                className=('text-center'))
as_of = html.Em(children=f'as at: {df.index[-1].year}-{df.index[-1].month}',
                className=('text-center'))





app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(title,width=12,class_name=('mt-4'))
    ]),
    dbc.Row([
        dbc.Col(as_of,width=12,class_name=('text-center mt-0 mb-4'))
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.surface_3d(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6,class_name=('mt-10')),

        dbc.Col(
            dcc.Graph(figure=data_viz.heatmap(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6)


    ]),


    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.line_yield_curve(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6),
        dbc.Col(
            dcc.Graph(figure=data_viz.line_spread(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6)
    ]),


],
                           fluid=True,
                           className="dbc")


####################################
# RUN the app
####################################
if __name__ == '__main__':
    server=app.server
    app.run_server(debug=True)
