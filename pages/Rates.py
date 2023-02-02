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

dash.register_page(__name__,name='US Treasuries') # Second Page

####################################
# Load data & dfs
####################################
df = get_data.get_rates()


####################################
# Page layout
####################################
as_of = html.Em(children=f'Data as of {df.index[-1].strftime("%b-%Y")}',
                className=('text-center'))

layout = dbc.Container([
    dbc.Row(as_of,class_name=('mb-4')),
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
            dcc.Graph(id='graph',figure=data_viz.line_yield_curve(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6),
        dbc.Col(
            dcc.Graph(figure=data_viz.line_spread(df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=6)
    ]),


],
                           fluid=True,
                           className="dbc")
