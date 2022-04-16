<img src="./figurl.png" width="200px" />

# figurl

Create shareable, interactive, live figures on the distributed web using Python

See also [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) and [figurl2-gui](https://github.com/scratchrealm/figurl2-gui).

## Quick static example

```python
# You'll first need to set up and configure kachery-cloud

# pip install altair vega_datasets

import figurl2 as fig

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

# Output: 
# https://v2.figurl.org/f?v=gs://figurl/vegalite-2&d=ipfs://bafkreibwifbjrcvxucu3o3373tz74jjkkee3u2t5wrbywzvcoc6q7lxs2i&label=stocks%20chart
```

[Resulting scatter plot](https://figurl.org/f?v=gs://figurl/vegalite-1&d=ipfs://bafkreierzdetqnlhxfczsz6zqg6psvjobzqidtgmhmf7a4z27gjkml32xq&label=scatter) with data stored in [Filebase](https://filebase.com/) and pinned on [IPFS](https://ipfs.io/).

## Other examples

The above is just a stack example. Figurl can do a lot more! Advanced examples coming soon.

## Introduction

[Introduction to Figurl](https://github.com/magland/figurl/wiki/Introduction-to-Figurl)

## Getting started

[Getting started with Figurl](https://github.com/magland/figurl/wiki/Getting-Started-with-Figurl)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
