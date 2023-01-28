import plotly.express as px
import figurl as fig

iris = px.data.iris()
ff = px.scatter_3d(iris, x='sepal_length', y='sepal_width', z='petal_width',
            color='species')

# Create and print the figURL
url = fig.Plotly(ff).url(label='plotly example - iris 3d')
print(url)

# Output: 
# https://figurl.org/f?v=gs://figurl/plotly-1&d=sha1://5c6ec276ce9a3b20b208aaff911b037ce4052e51&label=plotly%20example%20-%20iris%203d