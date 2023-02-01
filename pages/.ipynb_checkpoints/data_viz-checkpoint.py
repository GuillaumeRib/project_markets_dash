####################################
# DATA VIZ - CREATE CHARTS
####################################
import plotly.express as px
import pandas as pd

def sun(df,period='1M'):
    '''
    Plot a sunburst of S&P Sector industry and stocks by Size=weight, Color=Perf
    '''
    color_cont=['red','white','green']
    fig = px.sunburst(df,
                      path= ['Sector', 'Sub-Industry','Security'], #key arg for plotly to create hierarchy based on tidy data
                      values='Weight',
                      color=period,
                      color_continuous_scale=color_cont,
                      color_continuous_midpoint=0,
                      #range_color=[-0.5,0.5],
                      #hover_name=period,
                      hover_data={period:':.2%','Weight':':.2%'}
                      )
    fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'S&P 500 Breakdown | sector & industry - {period}',
                     height=600)
    return fig



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
                    size = 'Count',
                    hover_name='Sub-Industry',
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    hover_data={period:':.2%', 'Count':':.0f' }
                )
    fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Industry EW returns - {period}',
                     height=800,
                     xaxis_title=None,
                     yaxis_title=None
                     )

    fig.update_yaxes(tickformat='.0%')

    return fig


def tree(df,period='1M'):
    '''

    '''
    color_cont=['red','white','green']
    fig = px.treemap(df,
                     path= ['Sector','Sub-Industry','Security'], #key arg for plotly to create hierarchy based on tidy data
                     values='Weight',
                     color=period,
                     color_continuous_scale=color_cont,
                     color_continuous_midpoint=0,
                     #range_color=[-0.5,0.5],
                     hover_data={period:':.2%','Weight':':.2%'},
                     title=''
                 )

    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                     title=f'S&P 500 breakdown | Sector & industry - {period}'
                     )
    return fig

def bar_sec(df):
    '''

    '''
    df = df.groupby(by='Sector').mean()
    df= df.sort_values(by='YTD',ascending=False)

    fig = px.bar(df,
                 x=df.index,
                 y=['1M','3M','YTD'],
                 color_discrete_sequence=['darkgrey','grey','indianred'],
                 barmode='group',
                )

    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Sector EW returns',
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
                     y='3M',
                     color='Sector',
                     size='Weight',
                     hover_name='Security',
                     size_max=40,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     hover_data={'3M':':.2%',
                                 'YTD':':.2%',
                                 'Weight':':2%'},
                     title=f'Stock returns - 3M vs YTD'

                )
    fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                    )

    fig.update_yaxes(tickformat='.0%')
    fig.update_xaxes(tickformat='.0%')

    return fig

def line_sector(sector_cum_perf_df):
    '''
    Plot cumulative performances of Sectors(EW) vs EW of Sectors
    '''
    sectors = sector_cum_perf_df.columns
    fig = px.line(sector_cum_perf_df,
                     y=sectors,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     title=f'Cumulative growth | Sector EW - YTD'

                )

    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                     xaxis_title=None,
                     yaxis_title=None
                    )

    fig.update_yaxes(tickformat='.2f')


    return fig
