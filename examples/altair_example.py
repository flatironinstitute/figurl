import figurl as fig

import altair as alt
from vega_datasets import data

# Create an Altair chart
# This one comes from the Altair Example Gallery
stocks = data.stocks()

chart = alt.Chart(stocks).mark_line().encode(
  x='date:T',
  y='price',
  color='symbol'
).interactive(bind_y=False)

# Create and print the figURL
url = fig.Altair(chart).url(label='stocks chart')
print(url)

# Output: 
# https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart