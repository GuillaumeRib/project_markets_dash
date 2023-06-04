####################################
# DATA VIZ - CREATE CHARTS
####################################
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

####################################
############## RATES ###############
####################################

def line_yield_curve(df):
    '''
    Plot line chart of yield curve with animation, monthly
    '''
    df_rev = df.iloc[:, ::-1]
    tabular_df = pd.melt(df_rev.reset_index(), id_vars='DATE', value_vars=df_rev.columns, var_name='Maturity', value_name='Yield')
    tabular_df['DATE'] = tabular_df['DATE'].dt.strftime('%Y-%m')

    fig = px.line(tabular_df,
              x='Maturity',
              y='Yield',
              animation_frame='DATE',
              animation_group='Maturity',
              range_y=[0,7],
              markers='*',
              text=tabular_df.Yield,
             )
    fig.update_traces(mode='markers+text',
                  textposition='top center',
                  textfont=dict(
                                family='Arial',
                                size=14,
        )
    )
    fig.update_xaxes(title=None)
    fig.update_layout(title='Yield Curve Monthly Replay',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,
                  annotations=[
                            dict(
                                text="Data Source: FRED - Federal Reserve Economic Data",
                                x=0,
                                y=-0.15,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]
                  )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100
    #fig.show(animation=dict(fromcurrent=True,mode='immediate'))
    # Auto-play animation
    #plotly.offline.plot(fig, auto_play = True)
    return fig

def surface_3d(df):
    '''
    3d surface plot - History of Yield Curve on a monthly basis from 1m to 30Y rates
    '''

    fig = go.Figure(data=[go.Surface(x=df.columns,
                                    y=df.index,
                                    z=df.values,
                                    opacity=0.95,
                                    connectgaps=True,
                                    colorscale='rdbu',
                                    showscale=True,
                                    reversescale=True,
                                    )
                        ]
                )

    fig.update_layout(title='Yield Curve Historical Evolution',
                        title_font=dict(size = 20),
                        autosize=True,
                        #width=1600,
                        height=500,
                        hovermode='closest',
                        scene = {"aspectratio": {"x": 1, "y": 2.2, "z": 1},
                                'camera': {'eye':{'x': 2, 'y':0.4, 'z': 0.8}},
                                'xaxis_title':'Maturity',
                              'yaxis_title':'Date',
                              'zaxis_title':'Yield in %'
                                },
                        margin=dict(t=40),
                        annotations=[
                            dict(
                                text="Data Source: FRED - Federal Reserve Economic Data",
                                x=0,
                                y=-0.15,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]

                    )

    return fig

def line_spread(df):
    '''
    10-3MY spread over time
    '''
    data = df.copy()
    data['Spread'] = (df['10Y']-df['3M'])*100

    fig = px.area(data.reset_index(),
              x='DATE',
              y='Spread',
              range_y=[-200,400]

             )
    fig.update_xaxes(title=None)

    fig.update_layout(title='10Y-3M Spread in bps',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,
                  margin=dict(t=40),
                  annotations=[
                            dict(
                                text="Data Source: FRED - Federal Reserve Economic Data",
                                x=0,
                                y=-0.15,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]

                 )
    return fig

def heatmap2(df):
    '''
    imshow of yields per month per term in heatmap format
    '''
    data = df.T
    z = data * -1 # for colorscale to be reversed
    fig = px.imshow(z,
                    color_continuous_scale='rdbu',
                    )

    fig.update_xaxes(title=None)

    fig.update_layout(title='Yield Curve Heatmap',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,
                  coloraxis_showscale=False,
                  annotations=[
                            dict(
                                text="Data Source: FRED - Federal Reserve Economic Data",
                                x=0,
                                y=-0.15,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]
                 )

    fig.update_traces(hovertemplate='Date: %{x}<br>Maturity: %{y}<br>Value: %{z}',
                      customdata=data)
    return fig

def heatmap(df):
    '''
    imshow of yields per month per term in heatmap format
    '''
    data = df.T
    data=data.iloc[::-1] #to reverse order of rows in a df

    fig = go.Figure(data=[go.Heatmap(z=data.values,
                                     x=data.columns,
                                     y=data.index,

                                     colorscale='rdbu',
                                    showscale=True,
                                    reversescale=True,
                    )])

    fig.update_xaxes(title=None)

    fig.update_layout(title='Yield Curve Heatmap',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,
                  coloraxis_showscale=False,
                  margin=dict(t=38),
                  annotations=[
                            dict(
                                text="Data Source: FRED - Federal Reserve Economic Data",
                                x=0,
                                y=-0.15,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]
                 )
    return fig

####################################
############ EQUITIES ##############
####################################

def scat_ind(df,period='1M'):
    '''

    '''
    data = df.groupby(by=['Sub-Industry','Sector',],as_index=False).mean()
    count = df.groupby(by=['Sub-Industry','Sector'],as_index=False).count()
    data['Count'] = count.YTD
    data = data.sort_values(by=period,ascending=False)


    fig = px.scatter(data,
                    x='Sub-Industry',
                    y=period,
                    color='Sector',
                    size = 'Weight',
                    hover_name='Sub-Industry',
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    hover_data={period:':.2%', 'Weight':':.2%' }
                )
    fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Industry EW returns - {period}',
                      title_font=dict(size = 20),
                      autosize=True,
                     height=800,
                     xaxis_title=None,
                     yaxis_title=None
                     )

    fig.update_yaxes(tickformat='.0%')

    return fig

def tree(df,period='1M'):
    '''

    '''
    max_perf = df[period].max()
    color_cont=['red','white','green']
    fig = px.treemap(df,
                     path= ['Sector','Sub-Industry','Security'], #key arg for plotly to create hierarchy based on tidy data
                     values='Weight',
                     color=period,
                     color_continuous_scale=color_cont,
                     color_continuous_midpoint=0,

                     range_color=[-1.0,1],
                     hover_data={period:':.2%','Weight':':.2%'},
                     title=''
                 )

    fig.update_layout(margin=dict(l=20, r=20,),
                     height=600,
                     title=f'S&P 500 breakdown | Sector & industry - {period}',
                     title_font=dict(size = 20),
                     autosize=True,
                     annotations=[
                            dict(
                                text="Data Source: Yahoo Finance, Wikipedia, IVV ETF",
                                x=0,
                                y=-0.05,
                                xref="paper",
                                yref="paper",
                                showarrow=False
                            )
                        ]
                     )
    return fig

def bar_sec(df):
    '''

    '''
    df = df.groupby(by='Sector').mean()
    df= df.sort_values(by='YTD',ascending=False)

    fig = px.bar(df,
                 x=df.index,
                 y=['YTD','3M','2022'],
                 color_discrete_sequence=['indianred','grey','darkgrey'],
                 barmode='group',
                )

    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Sector EW returns',
                      title_font=dict(size = 20),
                      autosize=True,
                     height=600,
                     xaxis_title=None,
                     yaxis_title=None
                     )

    fig.update_yaxes(tickformat='.2%')

    return fig

def scat_stock(df):
    '''

    '''
    fig = px.scatter(df,
                     x='YTD',
                     y='1M',
                     color='Sector',
                     size='Weight',
                     hover_name='Security',
                     size_max=40,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     hover_data={
                         'Sub-Industry':True,
                         'YTD':':.2%',
                         '1M':':.2%',
                         'Weight':':2%'},
                     title=f'Stock returns - 1M vs YTD'

                )
    fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                     title_font=dict(size = 20),
                     autosize=True,
                    )

    fig.update_yaxes(tickformat='.0%')
    fig.update_xaxes(tickformat='.0%')

    return fig

def line_sector(sector_cum_perf_df):
    '''
    Plot cumulative performances of Sectors(EW) vs EW of Sectors
    '''
    data = sector_cum_perf_df.resample('W').mean()

    fig = px.line(data,
                     y=data.columns,
                     x=data.index,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     title=f'Cumulative growth | Sector EW - YTD'

                )


    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                     title_font=dict(size = 20),
                     autosize=True,
                     xaxis_title=None,
                     yaxis_title=None,
                    )

    fig.update_yaxes(tickformat='.2f')
    #fig.update_xaxes(
    #   rangebreaks=[dict(bounds=["sat","mon"]), #hide weekends - not rendering properly right now
    #    ]
    #)
    return fig
