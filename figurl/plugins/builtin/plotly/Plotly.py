import json
from typing import Union
from ....core.Figure import Figure

class Plotly(Figure):
    def __init__(self, figure):
        dd = {
            'type': 'Plotly',
            'spec': json.loads(figure.to_json())['data']
        }
        super().__init__(view_url='gs://figurl/plotly-1', data=dd)