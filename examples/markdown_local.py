import figurl as fig

source = '''
# Example markdown figure

To generate this figure, use something like the following

```python
import figurl as fig

source = '<define your markdown source>'

# Generate and print the figURL
url = fig.Markdown(source='...').url(label='Example markdown', local=True)
print(url)
```
'''

url = fig.Markdown(source=source).url(label='Example markdown', local=True)
print(url)
