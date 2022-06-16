<img src="../figurl.png" width="200px" />

# Introduction to Figurl

Figurl offers **browser-based**, **shareable**, **interactive** views of scientific
datasets in the cloud.

* [Overview](#overview)
* [Example: Static plot](#example-static-plot)
* [Example: Report](#example-report)
* [Example: Log table](#example-log-table)
* [Example: SortingView](#example-sortingview)
* [Example: Multi-trial spike train viewer](#example-multi-trial-spike-train-viewer)
* [Example: VolumeView](#example-volumeview)
* [Example: Tiled image](#example-tiled-image)
* [Example: Preview raw ephys traces](#example-preview-raw-ephys-traces)

## Overview

Generate a figURL (permalink) to an interactive visualization from a Python script

* Generate from anywhere: workstation, notebook, continuous integration, etc.
* Minimal configuration

Data needed for the visualization stored in the cloud

* See [kachery-cloud](https://github.com/scratchrealm/kachery-cloud)
* Content-addressable storage
* Configurable storage backend: Google, AWS, Wasabi, Filebase

Visualization plugin stored in cloud

* Domain-specific visualization plugins
* Versioned HTML bundles
* ReactJS / typescript - highly recommended but not strictly required

URL points to data and visualization plugin

* Data object is referenced via content-hash URI
* Visualization plugin is a static, versioned HTML bundle and is referenced by URI to a cloud bucket

Figurl web app ([figurl.org](https://figurl.org)) pairs the data with the visualization and presents the interactive view to the user

* Manages loading of data objects from the cloud
* Renders the visualization plugin in an embedded iframe
* Handles advanced capabilities of the figure
  - User login (e.g., for curation)
  - Lazy loading of additional data objects
  - Live feeds (for real-time updates or curation)
  - Task backends (for on-demand computation)

## Example: Static plot

The following simple example uses [Altair](https://altair-viz.github.io/), a Python wrapper around the [Vega-lite](http://vega.github.io/) visualization grammar. Any Altair chart can be turned into a figurl figure.

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
# https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart
```

Here's the [example script](../examples/altair_vegalite.py) a [link to the output figure](https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart).

Note that this script can be run from anywhere, and the output URL is shareable and archivable.

[![image](https://user-images.githubusercontent.com/3679296/174072660-2bdd8ed5-76bc-4272-9d9c-74ee039ee151.png)](https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart)

## Example: Report

A figurl report consists of a collection of sections that are laid out vertically in a scrollable figure. Sectioncan contain markdown text, static plots, and more advanced interactive figures.

[This report](https://figurl.org/f?v=gs://figurl/figurl-report&d=sha1://e0f267258f432adcb89c5379c4136c3f00fbce78&label=Example%20report) is the output of [this example script](../examples/report.py) and is self-explanatory.

Here's an [example report](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark) that documents the results of a benchmarking script for the [FINUFFT](https://finufft.readthedocs.io/en/latest/) project. See [finufft-benchmark](https://github.com/scratchrealm/finufft-benchmark).

[![image](https://user-images.githubusercontent.com/3679296/174073376-8eea5e6d-fba0-4461-bd37-bd49258ac54a.png)](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark)

## Example: Log table

This example shows how a figurl figure can update based on a live feed. This is useful for monitoring a lengthy computation or a live acquisition in real time.

```python
import time
import json
from datetime import datetime
import figurl as fig
import kachery_cloud as kcl


# Create a live feed
feed = kcl.create_feed()

# Create the LogTable figure and define the columns
X = fig.LogTable(feed)
X.add_column(key='iteration', label='Iteration')
X.add_column(key='timestamp', label='Timestamp')
X.add_column(key='text', label='Text')
X.add_column(key='data', label='Data')

# Print the figURL
url = X.url(label='Example logtable')
print(url)

# Add an iteration every few seconds (press Ctrl+C to terminate)
iteration = 1
while True:
    print(f'Appending message {iteration}')
    data = {
        'x': iteration,
        'y': iteration * iteration
    }
    feed.append_message({
        'iteration': iteration,
        'timestamp': f'{datetime.now()}',
        'text': f'Text for iteration {iteration}',
        'data': json.dumps(data)
    })
    iteration = iteration + 1
    time.sleep(5)

# Output:
# https://figurl.org/f?v=gs://figurl/logtable-1&d=sha1://fe780faacc5e9b74e4b26c3058a41ff24823a0e7&label=Example%20logtable
```

This example script can be [found here](../examples/logtable.py) and the [output figure is here](https://figurl.org/f?v=gs://figurl/logtable-1&d=sha1://fe780faacc5e9b74e4b26c3058a41ff24823a0e7&label=Example%20logtable). The script that generated this figure has already completed, so you won't see it updating in real time unless you run the script again yourself.

## Example: SortingView

The real power of figurl is the opportunity for domain-specific custom visualizations.

[SortingView](https://github.com/magland/sortingview) is built on figurl and allows users to view, curate, and share results of electrophysiological spike sorting in the browser. [Here is an example](https://www.figurl.org/f?v=gs://figurl/spikesortingview-4&d=sha1://a482c1e3c5575c8b9b27d12fedabc57266b378c0&project=lqhzprbdrq&label=Test%20workspace) figure that displays the output of spike sorting on a small simulated ephys dataset. Click the buttons in the upper-left corner to launch the various synchronized views. You can drag tabs between the top and bottom view areas.

This visualization also facilitates manual curation: labeling and merging of neural units. Each curation action is appended to a live feed hosted in the cloud. If two users are viewing the same SortingView figure, they will be able to collaborate on the curation and see live updates in real time. You need to be logged in as an authorized user to perform the curation.

[![image](https://user-images.githubusercontent.com/3679296/174078633-5672c3ed-e7ba-41c5-9506-739b9a146e63.png)](https://www.figurl.org/f?v=gs://figurl/spikesortingview-4&d=sha1://a482c1e3c5575c8b9b27d12fedabc57266b378c0&project=lqhzprbdrq&label=Test%20workspace)

## Example: Multi-trial spike train viewer

Here's another domain-specific figure in the area of electrophysiology and spike sorting.

See [multiscale-raster](https://github.com/scratchrealm/multitrial-raster). Here is a [sample output figure](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster). This visualization presents spike trains for hundreds of units over hundreds of trials. You can use the slider controls at the bottom to either view all units at once and slice through the trials, or view all the trials at once and slice through the units.

[![image](https://user-images.githubusercontent.com/3679296/174079122-20c29a95-17a5-4c5f-b503-16aa8bfc2683.png)](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster)

## Example: VolumeView

[VolumeView](https://github.com/magland/volumeview) is a figurl plugin for visualizing 3D volumetric data, vector fields, and surfaces.

Here are some example output figures:
* [cube](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreifwa43fxcsp463roznlnoaorwuxbopqkrkiheyyks56chcjmhp3r4&label=Test%20volumeview%20workspace)
* [grid scalar fields](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreiem7y6bactndiabma2c2nb2rtxyw5sv4xsbixgqn74pnmehxccwve&label=Test%20grid%20scalar%20fields)
* [grid vector field](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreig3jprc63qh25zv6si6cjh6a35tl72hp6ipwxdou3mvqrgvt3wbhu&label=Test%20grid%20vector%20field)
* [red blood cell surface](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreiflucxhbflk7s4v5l7coxj7prixec5a5z65gia4atpvuh2wtx6fxa&label=red%20blood%20cell)
* [paired red blood cell surfaces](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreifiln4dcb77xhjak3aqhk7awrryyvp4kpaslk7b2amx7j56lzjr2u&label=red%20blood%20cell)

[![image](https://user-images.githubusercontent.com/3679296/174079546-6c9171a1-3ffe-4589-81e7-2e56bab071eb.png)](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreig3jprc63qh25zv6si6cjh6a35tl72hp6ipwxdou3mvqrgvt3wbhu&label=Test%20grid%20vector%20field)

## Example: Tiled image

[figurl-tiled-image](https://github.com/scratchrealm/figurl-tiled-image) allows interactive visualization of very large images in a multi-scale zoomable tiled image display (Google maps style) using [deck.gl](https://deck.gl/). You can view a stack of images, and interactively toggle between the various layers.

Here's an [zoomable fractal image](https://figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=sha1://95755f9a7f02ab41fa03aff038bc97eff850d7a2&label=Mandelbrot%20tiled%20image).

Basic usage:

From Numpy array:

```python
import numpy as np
from figurl_tiled_image import TiledImage

array1 = ... # create a color image numpy array [N1 x N2 x 3] uint8
array2 = ... # create a color image numpy array [N1 x N2 x 3] uint8

X = TiledImage(tile_size=4096)
X.add_layer('layer 1', array1)
X.add_layer('layer 2', array2)
url = X.url(label='Numpy example')
print(url)
```

From image file:

```python
import pyvips
from figurl_tiled_image import TiledImage

filename1 = '/path/to/some/image1.png' # substitute the path to your image
image1 = pyvips.new_from_file(filename1)

filename2 = '/path/to/some/image2.png' # substitute the path to your image
image2 = pyvips.new_from_file(filename2)

X = TiledImage(tile_size=4096)
X.add_layer('layer 1', image1)
X.add_layer('layer 2', image2)
url = X.url(label='Example')
print(url)
```

[![image](https://user-images.githubusercontent.com/3679296/174079799-affffdc0-b09f-4750-b148-0d3aba48244b.png)](https://figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=sha1://95755f9a7f02ab41fa03aff038bc97eff850d7a2&label=Mandelbrot%20tiled%20image)

## Example: Preview raw ephys traces

The above TiledImage plugin can be used with [SpikeInterface](https://github.com/SpikeInterface/spikeinterface) to generate zoomable views of raw ephys data at various stages of preprocessing. This is useful for quality control and for inspecting the effects of filtering, denoising, etc. See [these notes](https://github.com/catalystneuro/spike-sorting-hackathon/tree/main/projects/visualizing-raw-data).

[This figure](https://www.figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=ipfs://QmRAkF6S2RWCxYDCjm5ov9LtxA4SivM1ETzHSphQAsRauv&label=SpikeInterface%20TiledImage%20example) represents Neuropixels 2.0 data after three different pre-processing steps (centering, filtering, and referencing).

[![image](https://user-images.githubusercontent.com/3679296/174080284-ecea8725-a778-4921-8579-4c2c13ee73f5.png)](https://www.figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=ipfs://QmRAkF6S2RWCxYDCjm5ov9LtxA4SivM1ETzHSphQAsRauv&label=SpikeInterface%20TiledImage%20example)
