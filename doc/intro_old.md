# Introduction to Figurl

Figurl offers **shareable**, **interactive**, **computation-backed** views of scientific
datasets in the cloud.

Figurl:

* Provides **domain-specific** views into **potentially large and complex datasets**
* Allows permalink sharing of interactive views of a **data snapshot** or of
**evolving data** (such as a streaming source or the results of live computations)
* Supports **reproducible data curation** or further dataset refinement
* Can **export** figures and their backing data to **stand-alone HTML bundles** suitable for
very-long-horizon archival services (under construction)

## What is Figurl?

Figurl provides a Python interface for publishing data objects together with the
visualization components that render the data, as well as a web application to display the
resulting views.

![Figurl ecosystem schematic diagram showing the various components discussed in this document](https://docs.google.com/drawings/d/e/2PACX-1vQ1EiWPmHTEzSQerCovx6LjHflUQ42BSrEg2c3LyFQzClmVoWgyNqaII9TT7W54DLC-AhteLMXWoq4V/pub?w=963&h=735)

This figure shows user-contributed elements in grey, outputs in blue, and Figurl-supplied elements in red. The full system comprises:

* The user's raw data (experimental results, etc)
* A user-contributed preprocessing script (to make the raw data suitable for viewing)
* The publication interface (call to `Figurl.Figure()`)
* A cloud-centered data distribution network
* A view or visualization component (either one of the Figurl-supplied general-purpose library components, or a custom module for a specific scientific domain)
* A web application (`figurl.org`) which fetches the viewable data and the visualization component and presents them together as a figure

Figurl generates permanent links to data-backed figures; we call these links figURLs.

Here's an example:
`https://www.figurl.org/f?v=gs://figurl/spikesortingview-2&d=ipfs://bafkreif3rb4yqpmece62wpfgqgdqc4izjitgs6x3htuqoeonwu6r5pd5ly&project=siojtbyvbw&label=Test%20workspace`

A figURL is a pairing between a *visualization component* (the `v` parameter in the URL query
string, `v=gs://figurl/spikesortingview-2`) and a *data object* that populates the
view (the `d` in the query string, here `d=ipfs://bafkreif3rb4yqpmece62wpfgqgdqc4izjitgs6x3htuqoeonwu6r5pd5ly`,
which is an IPFS hash URI of the data object).
The URL also encodes the *project ID* for more advanced interactions (live feeds, calculation tasks, and actions)
and an arbitrary *label* for the data being displayed
(`label=Test%20workspace`). The label
will be displayed on the figure view, but has no functional effect.

The visualization component can be part of the provided general-purpose library, or 
customized to the specific type of data being
displayed. Users from a wide range of fields can extend the set of available
visualization modules and share them with collaborators and the world at large.

The data parameter is the URI of a data object stored in and distributed by
[kachery-cloud](https://github.com/scatchrealm/kachery-cloud), a scientific data-sharing
tool developed at Flatiron by the authors of Figurl.

## Figurl generates shareable figures

"Shareable" means that you can send a link to a friend. You'll both see the same thing.

For example, this link:
https://figurl.org/f?v=gs://figurl/vegalite-2&d=ipfs://bafkreibwifbjrcvxucu3o3373tz74jjkkee3u2t5wrbywzvcoc6q7lxs2i&label=stocks%20chart

Should load the following image on any browser:

![Output for simple example plot used in Figurl introduction.](https://user-images.githubusercontent.com/3679296/167031737-acf5a03f-a318-4856-81a5-3ee41a0b80f7.png)

along with a surrounding frame from Figurl providing the file name and status information.

### Example: Generating a basic figure using Altair graphing library

FigURLs (the permalinks generated by Figurl) are created through a Python interface
that has access to a *data source* that provides the content to be visualized.
This data source is usually the result of applying some preprocessing steps (such as
sampling or normalization) to raw experimental data. The data source (after preprocessing) will be shared
through the kachery network; thus, the user creating the figURL needs to first [configure a kachery-cloud client](https://github.com/flatironinstitute/kachery-cloud).

The following code generates the simple example from above:

```python
# pip install altair vega_datasets

import figurl as fig

import altair as alt
from vega_datasets import data

# This script is adapted from an example on the Altair website
stocks = data.stocks()

# Create the Altair chart
chart = alt.Chart(stocks).mark_line().encode(
  x='date:T',
  y='price',
  color='symbol'
).interactive(bind_y=False)

# if running in a Jupyter notebook, the following
# line will also display the chart locally:
# display(chart)

# Generates and print the figURL permalink
url = fig.Altair(chart).url(label='stocks chart')
print(url)
```

As with many scripts that make use of Figurl, most of the Python code
is devoted to preparing the data (here using pandas and the Altair library).
The Figurl-specific part is the line:

```python
fig.Altair(chart).url(label='stocks chart')
```

which tells Figurl to publish the figure using the Altair visualization
module, a Figurl interface to the [Altair](https://altair-viz.github.io/)
declarative charting library. Internally, the Altair chart is configured
to a [Vega-lite](https://vega.github.io/vega-lite/) declarative specification.