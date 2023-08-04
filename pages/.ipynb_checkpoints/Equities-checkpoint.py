####################################
# IMPORTS
####################################

import pandas as pd
import datetime
import time

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from pages import get_data
from pages import data_viz
from pages.Rates import rates_update_time

dash.register_page(__name__) # Second page

####################################
# Load data & dfs
####################################
df = get_data.load_wiki_cons('pages/wiki_cons.csv')

weights = get_data.load_IVV_weight()
df = get_data.join_dfs(df,weights)
returns_df = get_data.get_returns()

# checking latest update Equities
equities_update_time = returns_df.index[-1].strftime("%b-%Y")

stock_df = get_data.get_stock_perf(returns_df,df)
sector_df, ind_df, sector_cum_perf = get_data.get_sector_perf(returns_df,df)

# new update time
equities_update_time = returns_df.index[-1].strftime("%b-%Y")

####################################
# Page layout
####################################

load_figure_template("lux")

as_of = html.Em(children=f'Data as of {equities_update_time}',
                className=('text-center'))

layout = dbc.Container([
    dbc.Row(as_of,class_name=('mb-4')),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.tree(stock_df,'YTD')),
            xs=12,sm=12,md=12,lg=12,xl=6,xxl=6,class_name=('mt-4')),
        dbc.Col(
            dcc.Graph(figure=data_viz.bar_sec(sector_df)),
            xs=12,sm=12,md=12,lg=12,xl=6,xxl=6,class_name=('mt-4')),
    ]),

    dbc.Row([
            dbc.Col(
                dcc.Graph(figure=data_viz.line_sector(sector_cum_perf)),
                xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
    ]),


    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.scat_stock(stock_df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
        dbc.Col(
            dcc.Graph(figure=data_viz.scat_ind(stock_df,'1M')),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
    ]),

],
                           fluid=True,
                           className="dbc")
