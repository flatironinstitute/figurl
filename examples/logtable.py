import time
from datetime import datetime
import figurl as fig
import kachery_cloud as kcl


# Create a live feed
feed = kcl.create_feed()

# Create the LogTable figure and define the columns
X = fig.LogTable(feed)
X.add_column(key='iteration', label='Iteration')
X.add_column(key='text', label='Text')

# Print the figURL
url = X.url(label='Example logtable')
print(url)

# Add an iteration every few seconds (press Ctrl+C to terminate)
iteration = 1
while True:
    print(f'Appending message {iteration}')
    feed.append_message({'iteration': iteration, 'text': f'Text for iteration {iteration}. Timestamp = {datetime.now()}'})
    iteration = iteration + 1
    time.sleep(5)

# Example output
# https://www.figurl.org/f?v=gs://figurl/logtable-1&d=ipfs://bafkreicnwdp627vnoibq7ebspcgdr72fslxypzkhvm42dqgom7ba27hdjm&label=Example%20logtable