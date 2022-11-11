import figurl as fig

source = '''
# Example markdown figure

To generate this figure, use something like the following

```python
import figurl as fig

source = '<define your markdown source>'

# Generate and print the figURL
url = fig.Markdown(source='...').url(label='Example markdown')
print(url)
```
'''

url = fig.Markdown(source=source).url(label='Example markdown')
print(url)

# Output:
# https://figurl.org/f?v=gs://figurl/markdown-1&d=sha1://9fe1d643f883e1676f70082b679c8a825b879041&label=Example%20markdown
