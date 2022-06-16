<img src="../figurl.png" width="200px" />

# Introduction to Figurl

Figurl offers **browser-based**, **shareable**, **interactive** views of scientific
datasets in the cloud.

* [Overview](#overview)
* [Examples](#examples)
  - [Static plot](#example-static-plot)
  - [Report](#example-report)
  - [Log table](#example-log-table)
  - [SortingView](#example-sortingview)
  - [Multi-trial spike train viewer](#example-multi-trial-spike-train-viewer)
  - [Multi-panel timeseries](#example-multi-panel-timeseries)
  - [Animal track animation](#example-animal-track-animation)
  - [VolumeView](#example-volumeview)
  - [Tiled image](#example-tiled-image)
  - [Preview raw ephys traces](#example-preview-raw-ephys-traces)
* [Advantages and discussion](#advantages-and-discussion)
  - [Shareable links](#shareable-links)
  - [Content addressable storage](#content-addressable-storage)
  - [Visualization plugins](#visualization-plugins)
* [Advanced capabilities](#advanced-capabilities)
  - [Live feeds](#live-feeds)
  - [Task backends](#task-backends)
* [Creating a visualization plugin](#creating-a-visualization-plugin)
* [Using your own cloud storage](#using-your-own-cloud-storage)

## Overview

<!-- https://docs.google.com/drawings/d/1mbB9KZ2Tq-PWOxIRYPc4OpPPDE5YF9U1HjIQ7H5bKJo/edit -->
![figurl overview](https://user-images.githubusercontent.com/3679296/174104842-cc3956bc-734b-4d38-85cc-f506e61092ec.png)

Figurl lets you use Python to generate a shareable figURL (permalink) to an interactive visualization.

* Generate from anywhere: workstation, notebook, continuous integration, etc.
* Minimal configuration

The data objects required for the visualization are stored in the cloud.

* See [kachery-cloud](https://github.com/scratchrealm/kachery-cloud)
* Content-addressable storage
* You can use our storage for free to get started (no configuration)
* Or configure your own storage bucket: Google, AWS, Wasabi, Filebase

The visualization plugin (HTML bundle) is also stored in the cloud.

* Domain-specific visualization plugins
* Versioned HTML bundles
* ReactJS / typescript - highly recommended but not strictly required
* Template available for creating custom visualizations

The shareable URL points uniquely to a data object and the visualization plugin.

* Data object is referenced via content-hash URI
* Visualization plugin is a static, versioned HTML bundle and is referenced by URI to a cloud bucket

The Figurl web app ([figurl.org](https://figurl.org)) pairs the data with the visualization and presents the interactive view to the user.

* Manages loading of data objects from the cloud
* Renders the visualization plugin in an embedded iframe
* Handles advanced capabilities of the figure
  - User login (e.g., for curation)
  - Lazy loading of additional data objects
  - Live feeds (for real-time updates or curation)
  - Task backends (for on-demand computation)

An optional backend service can be run in order to provide on-demand calculations and interacting with other advanced features of kachery-cloud such as live feeds.

## Examples

### Example: Static plot

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

### Example: Report

A figurl report consists of a collection of sections that are laid out vertically in a scrollable figure. Sectioncan contain markdown text, static plots, and more advanced interactive figures.

[This report](https://figurl.org/f?v=gs://figurl/figurl-report&d=sha1://e0f267258f432adcb89c5379c4136c3f00fbce78&label=Example%20report) is the output of [this example script](../examples/report.py) and is self-explanatory.

Here's an [example report](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark) that documents the results of a benchmarking script for the [FINUFFT](https://finufft.readthedocs.io/en/latest/) project. See [finufft-benchmark](https://github.com/scratchrealm/finufft-benchmark).

[![image](https://user-images.githubusercontent.com/3679296/174073376-8eea5e6d-fba0-4461-bd37-bd49258ac54a.png)](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark)

### Example: Log table

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

### Example: SortingView

The real power of figurl is the opportunity for domain-specific custom visualizations.

[SortingView](https://github.com/magland/sortingview) is built on figurl and allows users to view, curate, and share results of electrophysiological spike sorting in the browser. [Here is an example](https://www.figurl.org/f?v=gs://figurl/spikesortingview-4&d=sha1://a482c1e3c5575c8b9b27d12fedabc57266b378c0&project=lqhzprbdrq&label=Test%20workspace) figure that displays the output of spike sorting on a small simulated ephys dataset. Click the buttons in the upper-left corner to launch the various synchronized views. You can drag tabs between the top and bottom view areas.

This visualization also facilitates manual curation: labeling and merging of neural units. Each curation action is appended to a live feed hosted in the cloud. If two users are viewing the same SortingView figure, they will be able to collaborate on the curation and see live updates in real time. You need to be logged in as an authorized user to perform the curation.

[![image](https://user-images.githubusercontent.com/3679296/174078633-5672c3ed-e7ba-41c5-9506-739b9a146e63.png)](https://www.figurl.org/f?v=gs://figurl/spikesortingview-4&d=sha1://a482c1e3c5575c8b9b27d12fedabc57266b378c0&project=lqhzprbdrq&label=Test%20workspace)

### Example: Multi-trial spike train viewer

Here's another domain-specific figure in the area of electrophysiology and spike sorting.

See [multiscale-raster](https://github.com/scratchrealm/multitrial-raster). Here is a [sample output figure](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster). This visualization presents spike trains for hundreds of units over hundreds of trials. You can use the slider controls at the bottom to either view all units at once and slice through the trials, or view all the trials at once and slice through the units.

[![image](https://user-images.githubusercontent.com/3679296/174079122-20c29a95-17a5-4c5f-b503-16aa8bfc2683.png)](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster)

### Example: Multi-panel timeseries

Here's an example of multiple timeseries widgets that are stacked vertically. These are zoomable and synchronized. The top panel is a spike raster plot. The bottom panel uses a live backend to compute data on demand depending on the zoom activity of the user.

> Note: in this example, the backend will probably not be running at the time you are viewing it. Therefore, on the lower panel, only sections that have already been computed will be visible.

(Not publicly accessible at this time)

![image](https://user-images.githubusercontent.com/3679296/174131364-746554d1-adf3-40f7-a3ba-d5c5a47c700c.png)

### Example: Animal track animation

Animation of animal position on a track over time.

(Not publicly accessible at this time)

![image](https://user-images.githubusercontent.com/3679296/174148482-95fea08c-b5e9-4289-a002-9dc430719cc8.png)

### Example: VolumeView

[VolumeView](https://github.com/magland/volumeview) is a figurl plugin for visualizing 3D volumetric data, vector fields, and surfaces.

Here are some example output figures:
* [cube](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreifwa43fxcsp463roznlnoaorwuxbopqkrkiheyyks56chcjmhp3r4&label=Test%20volumeview%20workspace)
* [grid scalar fields](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreiem7y6bactndiabma2c2nb2rtxyw5sv4xsbixgqn74pnmehxccwve&label=Test%20grid%20scalar%20fields)
* [grid vector field](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreig3jprc63qh25zv6si6cjh6a35tl72hp6ipwxdou3mvqrgvt3wbhu&label=Test%20grid%20vector%20field)
* [red blood cell surface](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreiflucxhbflk7s4v5l7coxj7prixec5a5z65gia4atpvuh2wtx6fxa&label=red%20blood%20cell)
* [paired red blood cell surfaces](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreifiln4dcb77xhjak3aqhk7awrryyvp4kpaslk7b2amx7j56lzjr2u&label=red%20blood%20cell)

[![image](https://user-images.githubusercontent.com/3679296/174079546-6c9171a1-3ffe-4589-81e7-2e56bab071eb.png)](https://figurl.org/f?v=gs://figurl/volumeview-3&d=ipfs://bafkreig3jprc63qh25zv6si6cjh6a35tl72hp6ipwxdou3mvqrgvt3wbhu&label=Test%20grid%20vector%20field)

### Example: Tiled image

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

### Example: Preview raw ephys traces

The above TiledImage plugin can be used with [SpikeInterface](https://github.com/SpikeInterface/spikeinterface) to generate zoomable views of raw ephys data at various stages of preprocessing. This is useful for quality control and for inspecting the effects of filtering, denoising, etc. See [these notes](https://github.com/catalystneuro/spike-sorting-hackathon/tree/main/projects/visualizing-raw-data).

[This figure](https://www.figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=ipfs://QmRAkF6S2RWCxYDCjm5ov9LtxA4SivM1ETzHSphQAsRauv&label=SpikeInterface%20TiledImage%20example) represents Neuropixels 2.0 data after three different pre-processing steps (centering, filtering, and referencing).

[![image](https://user-images.githubusercontent.com/3679296/174080284-ecea8725-a778-4921-8579-4c2c13ee73f5.png)](https://www.figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=ipfs://QmRAkF6S2RWCxYDCjm5ov9LtxA4SivM1ETzHSphQAsRauv&label=SpikeInterface%20TiledImage%20example)

## Advantages and discussion

### Shareable links

The shareable link is perhaps the most portable, versatile, archiveable and robust method for sharing data, depending of course on the reliability and permanence of the content providing service. Because URLs are relatively short strings of text, they can be emailed, texted, uploaded to a database, or posted just about anywhere. As compared to working with files, URL links take up far less disk space, do not require special software for reading, and can be opened/launched from wherever they are found. Furthermore, assuming the backing resource is a reliable archive, they can even be embedded in publications or long-term archives.

Traditional software for scientific visualization does not produce such shareable URLs, but instead typically produces files that are either in common formats (pdf, png, svg) or in formats specific to certain software programs that must be installed and configured. Often, these software packages do not produce files at all, but interface directly with running processes. These factors limit where and how such software can be used. For example, some plotting libraries only work within Jupyter notebooks, or must be differently configured to operate in other settings. Cloud processes that run as part of continuous integration systems are limited in terms of how they can interact with external systems, and visualizations generated as outputs are typically not readily consumable.

In addition to the convenience and versatility of figURL links, web-based visualization software generally offers many advantages compared with desktop tools. The main advantage is that the web browser is inherently platform-independent, available on all desktop operating systems as well as on mobile devices. Another advantage is that web applications can be automatically upgraded without any action on the user's part. Other advantages relate to authentication, collaboration, and integration with cloud systems. While desktop software has some advantages in terms of performance and access to local on-disk datasets, for most applications, browser-based and cloud-based visualization tools are the most convenient for the end user and provide the greatest opportunities for integration and collaboration.

### Content-addressable storage

Figurl stores data in kachery-cloud which uses content-addressible URIs for locating files. Here is an example of a URI that points to a chunk of data in JSON format:

```
ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe
```

The string of characters is a content hash that uniquely points to the underlying file, like a fingerprint. The assumption is that no two files exist with the same content hash. This URI therefore points to the file by content and not by location. This is important for creating figURLs because we may want to move data around or change how it is accessed without invalidating URLs that have already been distributed or stored in a database. Here is a pointer to a figure that points to the above file as the `d` parameter in the query string:

https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark

It is also possible to retrieve that chunk of data directly from an [IPFS](https://ipfs.io/) gateway (assuming it still lives on the IPFS network):

https://ipfs.io/ipfs/bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe

Or we can retrieve it using the [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) command-line utility:

```bash
kachery-cloud-cat ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe
```

or from Python

```python
import kachery_cloud as kcl

a = kcl.load_json('ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe')
print(a)
```

Since we do not rely on any location-specific information to retrieve the file, we are free to change how and where we store the underlying data without invalidating the link. For example, if we want to publish the visualization via figURL, we could move the data to a long-term archival system.

Another advantage of using content hashes is that we have a means of verifying the integrity of the data file. When the file is downloaded, figurl (and kachery-cloud client) can check whether the content hash matches the URI.

While kachery-cloud and figurl can use IPFS for content-addressable storage, there are some disadvantages of relying on that distributed network. Therefore, the default is to use `sha1://` URIs instead, as can be seen in most of the above examples. While files are referenced via content URIs, the underlying data is usually stored in a cloud bucket (Google, AWS, Wasabi, or Filebase).

### Visualization plugins

The figurl web app (https://figurl.org) pairs the data object defined by the `d` query parameter in the figURL with the visualization plugin (`v` query parameter). The visualization plugin is a static HTML bundle, containing all the html and javascript files that have been compiled down from the ReactJS/typescript application. You can think of it as a binary executable that gets downloaded and executed by the web browser. The figurl web app loads the plugin into an embedded iframe and manages the interaction between the plugin and the kachery-cloud network (authentication, file downloads, live feeds, computation tasks, etc).

Usually the visualization plugin is hosted on a cloud storage bucket. For example, in the Altair plot of the basic example, it is hosted at `gs://figurl/vegalite-2` which is on a Google bucket. Note the `-2` at the end of this URI. If we want to make backward-compatible updates to the visualization that do not break any existing links (improve the layout, add features, etc), then we can just upload the new HTML bundle to that same location. However, if we want to make changes that break existing links (e.g., data spec adjustments), then we can increment that version number, upload the new bundle to `gs://figurl/vegalite-3`, and point future figURLs to the new location.

Visualization plugins are simply static websites that are embedded in the parent figurl.org web app. This is a big simplication compared with traditional websites that usually require a running server that provides a working API. The real work is performed by the parent figurl.org web application. This design is what allows us to store visualization plugins on storage buckets for long-term availability which is crucial for allowing figURLs to stay valid even as the visualization plugins are updated and improved over time.

## Advanced capabilities

### Live feeds

In addition to loading files that have been stored in kachery-cloud, visualizations can make use of live feeds. This is useful for viewing an ongoing process in real time, or for allowing the user to write to an append-only log (e.g., manual curation of a dataset).

This section needs to be finished.

### Task backends

It is not always possible or practical to precompute all data needed for a given visualization. Kachery-cloud task backends provide a means for computing data objects on demand based on user interactions.

This section needs to be finished.

## Creating a visualization plugin

This section needs to be written. For now, take a look at this template project which can be modified to build a custom visualization for figurl.

## Using your own cloud storage

By default, figurl will use our inexpensive cloud storage, and your data is not guaranteed to be available forever. However, it is also possible to configure your own cloud storage provider, which you pay for. This configuration is available in the web app at the time you configure your kachery-cloud client. We support Google, AWS, Wasabi and Filebase buckets. For more information see the [kachery-cloud documentation](https://github.com/scratchrealm/kachery-cloud).

https://github.com/scratchrealm/figurl-visualization-template

