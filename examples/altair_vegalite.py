# pip install altair vega_datasets

import figurl as fig

import altair as alt
from vega_datasets import data

stocks = data.stocks()

x = alt.Chart(stocks).mark_line().encode(
  x='date:T',
  y='price',
  color='symbol'
).interactive(bind_y=False)

url = fig.Altair(x).url(label='stocks chart')
print(url)