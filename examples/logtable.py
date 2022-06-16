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