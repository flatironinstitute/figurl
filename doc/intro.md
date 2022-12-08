<img src="../figurl.png" width="200px" />

# Introduction to Figurl

* [Overview](#overview)
* [Examples](#examples)
  - [Static plot](#example-static-plot)
  - [Report](#example-report)
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
* [Creating a visualization plugin](#creating-a-visualization-plugin)
* [Using your own cloud storage](#using-your-own-cloud-storage)

## Overview

<!-- https://docs.google.com/drawings/d/1mbB9KZ2Tq-PWOxIRYPc4OpPPDE5YF9U1HjIQ7H5bKJo/edit -->
![figurl overview](https://user-images.githubusercontent.com/3679296/174104842-cc3956bc-734b-4d38-85cc-f506e61092ec.png)

Figurl is a platform for creating and sharing interactive visualizations. From a Python script, users can create interactive browser-based figures that can immediately be shared simply by copy-pasting the link. The data needed for visualization is uploaded to the Kachery cloud and then retrieved by the browser to render using a custom visualization. Each domain-specific visualization plugin is a static HTML bundle that has been built using ReactJS / typescript. This plugin is embedded into the main figurl web application within an HTML iframe.

In addition to managing the flow of data from the cloud to the visualization, Figurl also handles advanced capabilities of the figure, such as user login for curation, GitHub integration, and lazy loading of additional data objects requested by the visualization plugin.

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

Here's the [example script](../examples/altair_example.py) a [link to the output figure](https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart).

Note that this script can be run from anywhere, and the output URL is shareable and archivable.

[![image](https://user-images.githubusercontent.com/3679296/174072660-2bdd8ed5-76bc-4272-9d9c-74ee039ee151.png)](https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart)

### Example: Report

A figurl report consists of a collection of sections that are laid out vertically in a scrollable figure. Sectioncan contain markdown text, static plots, and more advanced interactive figures.

[This report](https://figurl.org/f?v=gs://figurl/figurl-report&d=sha1://e0f267258f432adcb89c5379c4136c3f00fbce78&label=Example%20report) is the output of [this example script](../examples/report_example.py) and is self-explanatory.

Here's an [example report](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark) that documents the results of a benchmarking script for the [FINUFFT](https://finufft.readthedocs.io/en/latest/) project. See [finufft-benchmark](https://github.com/scratchrealm/finufft-benchmark).

[![image](https://user-images.githubusercontent.com/3679296/174073376-8eea5e6d-fba0-4461-bd37-bd49258ac54a.png)](https://www.figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark)

### Example: SortingView

The real power of figurl is the opportunity for domain-specific custom visualizations.

[SortingView](https://github.com/magland/sortingview) is built on figurl and allows users to view, curate, and share results of electrophysiological spike sorting in the browser. [Here is an example](https://figurl.org/f?v=gs://figurl/spikesortingview-10&d=zenodo://7195410/main&label=First%20Zenodo%20FigURL) figure that displays the output of spike sorting on a small simulated ephys dataset. Click the buttons in the upper-left corner to launch the various synchronized views. You can drag tabs between the top and bottom view areas.

This visualization also facilitates manual curation: labeling and merging of neural units.

[![image](https://user-images.githubusercontent.com/3679296/174078633-5672c3ed-e7ba-41c5-9506-739b9a146e63.png)](https://www.figurl.org/f?v=gs://figurl/spikesortingview-4&d=sha1://a482c1e3c5575c8b9b27d12fedabc57266b378c0&project=lqhzprbdrq&label=Test%20workspace)

### Example: Multi-trial spike train viewer

Here's another domain-specific figure in the area of electrophysiology and spike sorting.

See [multitrial-raster](https://github.com/scratchrealm/multitrial-raster). Here is a [sample output figure](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster). This visualization presents spike trains for hundreds of units over hundreds of trials. You can use the slider controls at the bottom to either view all units at once and slice through the trials, or view all the trials at once and slice through the units.

[![image](https://user-images.githubusercontent.com/3679296/174079122-20c29a95-17a5-4c5f-b503-16aa8bfc2683.png)](https://www.figurl.org/f?v=gs://figurl/multitrial-raster-2&d=sha1://8a9686064f3cf7758c678defa3902094790af76c&label=Multi-trial%20raster)

### Example: Multi-panel timeseries

Here's an example of multiple timeseries widgets that are stacked vertically. These are zoomable and synchronized. The top panel is a spike raster plot. The bottom panel uses a live backend to compute data on demand depending on the zoom activity of the user.

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

Here's an example of [60 seconds of Neuropixels raw data](https://www.figurl.org/f?v=gs://figurl/tiled-image-1&d=ipfs://QmSd9GRVwpeQ4hfH5gZfhH48GFZYzYD3XjSdmrdkadBhEF&label=Neuropix-PXI-100_ProbeA-AP%20-%2060%20seconds) (384 channels). This is more than 1 GB of data efficiently loaded into the browser (Google maps style).

## Advantages and discussion

### Shareable links

The shareable link is one of the most convenient and reliable ways to share information. With their brief and concise code, URLs can be sent via email, text, stored in databases or shared anywhere else. Additionally, links occupy far less storage space than conventional figures, don't need special programs to access them and can be opened from any location with internet access. What's more, if the content's source is a reliable archive, URLs can even be added to publications or kept in permanent storage.

Traditional software programs used for scientific visualization generally produce files rather than URLs. These files can be in well-known (non-interactive) formats (such as pdf, png, or svg), or in formats specific to a particular application, requiring installation and configuration. In some cases, no files are created at all, and the software simply interacts with an existing process. This makes it difficult to use the software in various locations and settings; for example, some plotting libraries work only in Jupyter notebooks, and need to be adjusted for other settings. Cloud-based processes as part of continuous integration systems also have limited interaction with external systems, and the visualization files they generate are not always easy to obtain or open.

Besides the flexibility and ease of use of figURL links, web-based visualizing programs offer a variety of advantages when compared to desktop tools. The primary benefit is that web browsers are compatible across all desktop and mobile operating systems. Additionally, web applications can be updated without any input from the user. Other advantages include authentication, teamwork, and integration with cloud systems. While desktop software provides some advantages in terms of access to local data, in most cases, browser-based and cloud-based visualization tools are the most practical for a user and provide the greatest chances of collaboration and integration.

### Content-addressable storage

Figurl stores data in kachery-cloud which uses content-addressible URIs for locating files. Here is an example of a URI that points to a chunk of data in JSON format:

```
sha1://21df8ad1fd24b9d9ad112b70de5cd5f7cd67d2a8
```

The string of characters is a content hash that uniquely points to the underlying file, like a fingerprint. The assumption is that no two files exist with the same content hash. This URI therefore points to the file by content and not by location. This is important for creating figURLs because we may want to move data around or change how it is accessed without invalidating URLs that have already been distributed or stored in a database. Here is a pointer to a figure that uses the above file as the `d` parameter in the query string:

https://www.figurl.org/f?v=gs://figurl/figurl-report&d=sha1://21df8ad1fd24b9d9ad112b70de5cd5f7cd67d2a8&label=FINUFFT%20benchmark

It is also possible to retrieve that chunk of data directly from Kachery cloud using the Python or command-line interface:

```bash
kachery-cloud-cat sha1://21df8ad1fd24b9d9ad112b70de5cd5f7cd67d2a8
```

```python
import kachery_cloud as kcl

a = kcl.load_json('sha1://21df8ad1fd24b9d9ad112b70de5cd5f7cd67d2a8')
print(a)
```

Since we do not use location-specific data to access the file, we can shift where and how the data is kept without invalidating the link. For instance, if we decide to publish the visualization, we could transfer the data to a long-term storage system. The link would stay the same.

Another advantage of employing content hashes is that we have the ability to validate the accuracy of the data file. When the file is obtained, figurl (and the Kachery client) can verify whether the content hash corresponds to the URI.

TODO: talk about why we don't use IPFS

### Visualization plugins

The figurl web app (https://figurl.org) pairs the data object defined by the `d` query parameter in the figURL with the visualization plugin (`v` query parameter). The visualization plugin is a static HTML bundle, containing all the html and javascript files that have been compiled down from the ReactJS/typescript application. You can think of it as a binary executable that gets downloaded and executed by the web browser. The figurl web app loads the plugin into an embedded iframe and manages the interaction between the plugin and the kachery-cloud network (authentication, file downloads, etc).

Usually the visualization plugin is hosted on a cloud storage bucket. For example, in the Altair plot of the basic example, it is found at `gs://figurl/vegalite-2` on a Google bucket (note the `-2` at the end of the URI). If we want to make updates to the visualization that will not affect existing links (improve the layout, add features, etc.), then the new HTML bundle can be uploaded to the same place. However, if the changes made will break existing links (e.g., data spec adjustments), then the version number should be incremented, the new bundle uploaded to `gs://figurl/vegalite-3`, and all future figURLs pointed to the new location.

Visualization plugins are simply static websites that are embedded in the parent figurl.org web app. This is a big simplification compared with traditional websites that usually require a running server that provides a working API. The real work is performed by the parent figurl.org web application. This design is what allows us to store visualization plugins on storage buckets for long-term availability which is crucial for allowing figURLs to stay valid even as the visualization plugins are updated and improved over time.

## Creating a visualization plugin

TODO: This section needs to be written. Contact us for more information on creating your own Figurl visualization plugin.

## Using your own cloud storage

By default, your data files will be stored using our cloud resources, and they are not guaranteed to be available forever. You can also configure figurl to use your own storage buckets by [creating a Kachery zone](https://github.com/flatironinstitute/kachery-cloud/blob/main/doc/create_kachery_zone.md).