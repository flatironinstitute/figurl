from typing import Any, List, Union
import altair
from figurl.core.Figure import Figure


class ReportItem:
    def __init__(self, item_type: str, data: Any) -> None:
        self._item_type = item_type
        self._data = data
        if item_type == 'markdown':
            assert isinstance(data, dict) and 'source' in data and isinstance(data['source'], str)
        elif item_type == 'altair_chart':
            assert isinstance(data, dict) and 'spec' in data
        else:
            raise Exception(f'Invalid item type')
    def to_dict(self):
        return {
            'type': self._item_type,
            'data': self._data
        }

class ReportItemContainer:
    def __init__(self) -> None:
        self._items: List[Union[ReportItem, ReportHBoxLayout]] = []
    def add_altair_chart(self, chart: altair.Chart):
        self._items.append(ReportItem(
            'altair_chart',
            {
                'spec': chart.to_dict()
            }
        ))
    def add_markdown(self, markdown: str):
        self._items.append(ReportItem(
            'markdown',
            {
                'source': markdown
            }
        ))
    def add_hboxlayout(self):
        layout = ReportHBoxLayout()
        self._items.append(layout)
        return layout

class ReportHBoxLayout(ReportItemContainer):
    def __init__(self) -> None:
        super().__init__()
    def to_dict(self):
        return {
            'type': 'hboxlayout',
            'data': {
                'items': [
                    item.to_dict()
                    for item in self._items
                ]
            }
        }

class Report(ReportItemContainer):
    def __init__(self) -> None:
        super().__init__()
    def to_dict(self):
        return {
            'items': [
                item.to_dict()
                for item in self._items
            ]
        }
    def url(self, *, label: str):
        F = Figure(
            view_url='gs://figurl/figurl-report',
            data=self.to_dict()
        )
        return F.url(label=label)