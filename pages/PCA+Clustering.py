####################################
# IMPORTS
####################################

import pandas as pd
import numpy as np
import datetime
import time

import dash
from dash import dcc
from dash import html,callback,Input,Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
from plotly.subplots import make_subplots

from pages import get_data
from pages import data_viz
from pages.Rates import rates_update_time

dash.register_page(__name__) # Third page

####################################
# Load data & dfs
####################################
df = get_data.load_wiki_cons('pages/wiki_cons.csv')

weights = get_data.load_IVV_weight()
df = get_data.join_dfs(df,weights)
X = get_data.get_spx_returns(freq='D')
print(X.shape[0])
X = X.tail(252*2)
print(X.index[-1])

def update_graph(value1=10, value2=11):
    W,pca,X_proj,cum_var = get_data.train_PCA(X,n_comp=value1)
    clusters = get_data.get_pcakmean_clusters(W,k=value2)
    cum_var_max = "{:.2f}".format(cum_var.max()*100)

    # Plot total cumulative explained variance using n_comp PCs
    W_clust = W.join(clusters).join(df)
    W_clust["cluster"] = W_clust["cluster"].astype(str)

    fig1 = px.bar(cum_var,
                  height=350,
              title=f'Cumulative Variance explained by {value1} PCs: {cum_var_max}%',
             )
    fig1.update_layout(xaxis_title='PCs', yaxis_title='Cum Var', showlegend=False)

    fig2 = px.scatter_3d(W_clust, x='PC1', y='PC2', z='PC3',
                    height=700,
                    color='cluster',
                    hover_data=[W_clust.index,W_clust.Security,W_clust.cluster],
                    title=f'Top 3 PCs loadings and {value2} clusters visualization',
                    color_discrete_sequence=px.colors.qualitative.Safe
                   )
    fig2.update_layout(scene=dict(
    aspectmode='cube'
    )),

    # Plot Correlation Heatmaps
    fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Unclustered Stocks',
                                                    'Clustered Stocks'
                                    ))
    heatmap1 = px.imshow(X.corr(),aspect='equal')
    heatmap2 = px.imshow(X[clusters.index].corr(),aspect='equal')
    fig3.add_trace(heatmap1.data[0], row=1, col=1)
    fig3.add_trace(heatmap2.data[0], row=1, col=2)
    # Set square aspect ratio for each subplot
    fig3.update_xaxes(scaleanchor='y', scaleratio=1, row=1, col=1)
    fig3.update_yaxes(scaleanchor='x', scaleratio=1, row=1, col=1)
    fig3.update_xaxes(scaleanchor='y', scaleratio=1, row=1, col=2)
    fig3.update_yaxes(scaleanchor='x', scaleratio=1, row=1, col=2)

    fig3.update_layout(showlegend=True,
                    coloraxis={'colorscale': 'viridis'},
                    title='Correlation Heatmaps Comparison',
                    )


    # Clustering details
    data = clusters.join(df)
    grouped = data.groupby(['cluster', 'Sector', 'Security']).size().reset_index(name='count')
    fig4 = px.bar(grouped, x='cluster', y='count', color='Sector', title=f'Cluster details by Security and GICS Sector',
                barmode='stack',hover_data=['Security'],text='Security',
                height=700,
                )
    fig4.update_layout(xaxis_title='Cluster', yaxis_title='Security count', hovermode='closest')

    return fig1, fig3, fig2, fig4

fig1, fig3, fig2, fig4 = update_graph()

# new update time
equities_update_time = X.index[-1].strftime("%b-%Y")

####################################
# Page layout
####################################

load_figure_template("lux")

as_of = html.Em(children=f'Data as of {equities_update_time}',
                className=('text-center'))

layout = dbc.Container([
    dbc.Row(as_of,class_name=('mb-4')),
    dbc.Row(
        html.P(
            children="K-Means clustering of S&P 500 stocks using Principal Component Analysis.",
            style={'fontSize':16}
            )
        ),
    dbc.Row(html.P(children="Based on daily total returns over the past 2Yrs",
                style={'fontSize':12})),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig1),xs=12,sm=12,md=12,lg=4,xl=4,xxl=4,class_name=('mt-4')),

        dbc.Col(
            dcc.Graph(figure=fig3),xs=12,sm=12,md=12,lg=8,xl=8,xxl=8,class_name=('mt-4')
            ),
    ]),

    dbc.Row([
            dbc.Col(dcc.Graph(figure=fig2),width=10),
            ],justify='center'),
    dbc.Row([
            dbc.Col(dcc.Graph(figure=fig4),width=10),
            ],justify='center')
    ],
                       fluid=True,
                       className="dbc")


def update_graph(value1=10, value2=25):
    W,pca,X_proj,cum_var = get_data.train_PCA(X,n_comp=value1)
    clusters = get_data.get_pcakmean_clusters(W,k=value2)
    cum_var_max = "{:.2f}".format(cum_var.max()*100)

    # Plot total cumulative explained variance using n_comp PCs
    W_clust = W.join(clusters).join(df)
    W_clust["cluster"] = W_clust["cluster"].astype(str)

    fig1 = px.bar(cum_var,
                  height=350,
              title=f'Cumulative Variance explained by {value1} PCs: {cum_var_max}%',
             )
    fig1.update_layout(xaxis_title='PCs', yaxis_title='Cum Var', showlegend=False)

    fig2 = px.scatter_3d(W_clust, x='PC1', y='PC2', z='PC3',
                    height=700,
                    color='cluster',
                    hover_data=[W_clust.index,W_clust.Security,W_clust.cluster],
                    title=f'Top 3 PCs loadings and {value2} clusters visualization',
                    color_discrete_sequence=px.colors.qualitative.Safe
                   )
    fig2.update_layout(scene=dict(
    aspectmode='cube'
    )),

    # Plot Correlation Heatmaps
    fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Unclustered Stocks',
                                                    'Clustered Stocks'
                                    ))
    heatmap1 = px.imshow(X.corr(),aspect='equal')
    heatmap2 = px.imshow(X[clusters.index].corr(),aspect='equal')
    fig3.add_trace(heatmap1.data[0], row=1, col=1)
    fig3.add_trace(heatmap2.data[0], row=1, col=2)
    # Set square aspect ratio for each subplot
    fig3.update_xaxes(scaleanchor='y', scaleratio=1, row=1, col=1)
    fig3.update_yaxes(scaleanchor='x', scaleratio=1, row=1, col=1)
    fig3.update_xaxes(scaleanchor='y', scaleratio=1, row=1, col=2)
    fig3.update_yaxes(scaleanchor='x', scaleratio=1, row=1, col=2)

    fig3.update_layout(showlegend=True,
                    coloraxis={'colorscale': 'viridis'},
                    title='Correlation Heatmaps Comparison',
                    )


    # Clustering details
    data = clusters.join(df)
    grouped = data.groupby(['cluster', 'Sector', 'Security']).size().reset_index(name='count')
    fig4 = px.bar(grouped, x='cluster', y='count', color='Sector', title=f'Cluster details by Security and GICS Sector',
                barmode='stack',hover_data=['Security'],text='Security',
                height=700,
                )
    fig4.update_layout(xaxis_title='Cluster', yaxis_title='Security count', hovermode='closest')

    return fig1, fig3, fig2, fig4
