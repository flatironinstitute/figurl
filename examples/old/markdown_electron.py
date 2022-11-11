import figurl as fig

source = '''
# Example markdown figure

To generate this figure, use something like the following

```python
import figurl as fig

source = '<define your markdown source>'

# Open electron app
fig.Markdown(source='...').electron(label='Example markdown')
```
'''

fig.Markdown(source=source).electron(label='Example markdown')
