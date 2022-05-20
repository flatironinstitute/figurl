<img src="./figurl.png" width="200px" />

# figurl

Create web-shareable, interactive, live figures using Python.

See also [kachery-cloud](https://github.com/scratchrealm/kachery-cloud)

## Installation and setup

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

```bash
pip install --upgrade figurl
```

Configure your [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) client

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

## Example: Static plot

```bash
pip install altair vega_datasets
```

```python
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
# https://figurl.org/f?v=gs://figurl/vegalite-2&d=ipfs://bafkreibwifbjrcvxucu3o3373tz74jjkkee3u2t5wrbywzvcoc6q7lxs2i&label=stocks%20chart
```

Here is the [resulting plot](https://figurl.org/f?v=gs://figurl/vegalite-2&d=ipfs://bafkreibwifbjrcvxucu3o3373tz74jjkkee3u2t5wrbywzvcoc6q7lxs2i&label=stocks%20chart) with data pinned on [IPFS](https://ipfs.io/).

## Example: Log table from a live feed

```python
import time
from datetime import datetime
import figurl as fig
import kachery_cloud as kcl


# Create a live feed
feed = kcl.create_feed()

# Create the LogTable figure and define the columns
X = fig.LogTable(feed)
X.add_column(key='iteration', label='Iteration')
X.add_column(key='text', label='Text')

# Print the figURL
url = X.url(label='Example logtable')
print(url)

# Add an iteration every few seconds (press Ctrl+C to terminate)
iteration = 1
while True:
    print(f'Appending message {iteration}')
    feed.append_message({'iteration': iteration, 'text': f'Text for iteration {iteration}. Timestamp = {datetime.now()}'})
    iteration = iteration + 1
    time.sleep(5)

# Example output
# https://www.figurl.org/f?v=gs://figurl/logtable-1&d=ipfs://bafkreicnwdp627vnoibq7ebspcgdr72fslxypzkhvm42dqgom7ba27hdjm&label=Example%20logtable
```

Here is the resulting [log table](https://www.figurl.org/f?v=gs://figurl/logtable-1&d=ipfs://bafkreicnwdp627vnoibq7ebspcgdr72fslxypzkhvm42dqgom7ba27hdjm&label=Example%20logtable). The program has been terminated so it won't be live-updating, but you can run the script to create a new live-updating example.

## Reports

See [examples/report.py](examples/report.py) which generates [this report figure](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreie7peuiujotcwcicgharaucsg7qmadmmdfmwjtbr3ilm263ihbh4q&label=Example%20report).

## Other examples

See [these examples](./examples/).

The following projects use Figurl

* [VolumeView](https://github.com/magland/volumeview)
* [SortingView](https://github.com/magland/sortingview/tree/v2)
* [TiledImage](https://github.com/scratchrealm/figurl-tiled-image)
* [finufft-benchmark](https://github.com/scratchrealm/finufft-benchmark)

Figurl can do a lot more! Further examples coming soon.

## Introduction

[Introduction to Figurl](doc/intro.md)

## Information for developers

See [figurl2-gui](https://github.com/scratchrealm/figurl2-gui)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
