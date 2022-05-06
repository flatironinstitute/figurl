import kachery_cloud as kcl
from ....core.Figure import Figure

class LogTable(Figure):
    def __init__(self, feed: kcl.Feed):
        data = {
            'feedUri': feed.uri
        }
        super().__init__(view_url='gs://figurl/logtable-1', data=data)
    def add_column(self, *, key: str, label: str):
        data = super().data
        if 'columns' not in data:
            data['columns'] = []
        data['columns'].append({
            'key': key,
            'label': label
        })
        super().set_data(data)