import altair as alt
from vega_datasets import data
import figurl as fig

report = fig.Report()

report.add_markdown('''
# Example report

A figurl report consists of a collection of sections
that are laid out vertically in a scrollable figure.

First initiate the report:

```python
import figurl as fig

report = fig.Report()
```

Add a markdown item:

```python
source = '...'
report.add_markdown(source)
```

Add a chart:

```python
chart = ... # define an altair chart
report.add_altair_chart(chart)
```

Add more markdown:

```python
report.add_markdown('...')
```

Generate the figURL

```python
url = report.url(label='Example report')
print(url)
```

Here is an example chart:
''')

# Add an altair chart
iris = data.iris()
chart = alt.Chart(iris).mark_point().encode(
    x='petalLength',
    y='petalWidth',
    color='species'
)
report.add_altair_chart(chart)

report.add_markdown('''
## Horizontal layouts

You can also add horizontal layout items and insert items
onto the layout:

```python
chart1 = ... # define an altair chart
chart2 = ... # define an altair chart
layout = report.add_hboxlayout()
layout.add_altair_chart(chart1)
layout.add_altair_chart(chart2)
```

Here is an example horizontal layout item:
''')

chart1 = chart
chart2 = chart
layout = report.add_hboxlayout()
layout.add_altair_chart(chart1)
layout.add_altair_chart(chart2)

url = report.url(label='Example report')
print(url)
