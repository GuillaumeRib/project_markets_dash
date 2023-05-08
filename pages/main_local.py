####################################
# MAIN PAGE
####################################
import plotly.express as px
import pandas as pd
import get_data

# Run Main to update prices & constituents


if __name__ == '__main__':
    print('main')

    # To Update constituents from Wiki
    get_data.get_spx_cons('wiki_cons.csv')

    # To Update latest prices
    df = get_data.load_wiki_cons('wiki_cons.csv')
    get_data.get_prices(df)
