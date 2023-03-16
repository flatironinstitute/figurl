import os
import subprocess
import json
from typing import Any, Union
import urllib.parse
import kachery_cloud as kcl
from .serialize_wrapper import _serialize

def url_from_url_dict(url_dict: dict, *, base_url: Union[str, None]=None):
    if base_url is None:
        base_url = default_base_url
    dd = url_dict
    url = f'{base_url}/f?v={dd["v"]}&d={dd["d"]}'
    if dd.get('hide'):
        url += '&hide=1'
    if dd.get('state'):
        url += f'&s={dd["state"]}'
    if dd.get('sh'):
        url += f'&sh={dd["sh"]}'
    if dd.get('dir'):
        url += f'&sh={dd["dir"]}'
    if dd.get('label'):
        url += f'&label={_enc(dd["label"])}'
    if dd.get('zone'):
        url += f'&zone={_enc(dd["zone"])}'
    return url


class Figure:
    def __init__(self, *, data: Any, view_url: Union[str, None]=None, access_group: Union[str, None]=None, state: Union[dict, None]=None, sh: Union[str, None]=None, dir: Union[str, None]=None):
        self._view_url = view_url
        self._data = data
        self._state = state
        self._serialized_data = _serialize(self._data, compress_npy=True)
        self._access_group = access_group
        self._sh = sh
        self._dir = dir

        if state is not None:
            print('DEPRECATION WARNING: pass state parameter into url() rather than constructor for figurl Figure')

        # check up front whether figure data is too large
        max_data_size = 500 * 1000 * 1000
        data_size = len(json.dumps(self._serialized_data))
        if data_size > max_data_size:
            raise Exception(f'Figure data is too large ({data_size} > {max_data_size} bytes). A live view is probably in order for this figure.')

        if view_url is not None:
            self._object = None
        else:
            raise Exception('Missing view_url')
        self._data_uri: Union[str, None] = None # new system
    @property
    def object(self):
        return self._object
    @property
    def view_url(self):
        return self._view_url # new system
    @property
    def data(self):
        return self._data
    @property
    def state(self):
        return self._state
    def set_data(self, data: Any):
        self._data = data
        self._serialized_data = _serialize(data, compress_npy=True)
    def set_state(self, state: Union[dict, None]):
        self._state = state
    def url_dict(self, *, label: str, view_url: Union[str, None] = None, hide_app_bar: bool=False, state: Union[None, dict]=None):
        if state is not None:
            self._state = state
        if self._state is not None:
            import simplejson
            state_json = simplejson.dumps(self._state, separators=(',', ':'), indent=None, allow_nan=False, sort_keys=True)
        else:
            state_json = None
        self._data_uri = kcl.store_json(self._serialized_data)
        if self._access_group is not None:
            self._data_uri = kcl.encrypt_uri(self._data_uri, access_group=self._access_group)
        data_uri = self._data_uri
        if view_url is None:
            view_url = self._view_url
        if view_url is None:
            raise Exception('No view URL')
        ret = {
            'type': 'figurl',
            'label': label,
            'v': view_url,
            'd': data_uri
        }
        if state_json is not None:
            ret['state'] = state_json
        if hide_app_bar:
            ret['hide'] = True
        zone_name = os.getenv('KACHERY_ZONE', None)
        if zone_name is not None:
            ret['zone'] = zone_name
        if self._sh:
            ret['sh'] = self._sh
        if self._dir:
            ret['dir'] = self._dir
        return ret
    def url(self, *, label: str, base_url: Union[str, None]=None, view_url: Union[str, None] = None, hide_app_bar: bool=False, state: Union[None, dict]=None):
        dd = self.url_dict(label=label, view_url=view_url, hide_app_bar=hide_app_bar, state=state)
        return url_from_url_dict(dd)
    # def electron(self, *, label: str, listen_port: Union[int, None]=None):
    #     url = self.url(label=label, local=True) # important to use local
    #     query = _parse_url(url)
    #     vv = query['v']
    #     dd = query['d']
    #     label = query.get('label', '')
    #     cmd = f'figurl-electron -d {dd} -v {vv}'
    #     if label:
    #         cmd = cmd + f' --label {label}'
    #     if listen_port is not None:
    #         cmd = cmd + f' --listenPort {listen_port}'

    #     # this is important because $HOME sometimes gets remapped with electron
    #     env = os.environ.copy()
    #     env["KACHERY_CLOUD_DIR"] = kcl.get_kachery_cloud_dir()

    #     # retcode = subprocess.run(cmd.split(' '), env=env, check=True).returncode
    #     # if retcode != 0:
    #     #     print('Error running electron app. Is figurl-electron installed?')
    #     subprocess.Popen(cmd.split(' '), env=env)

def _parse_url(url: str):
    query = {}
    ind1 = url.index('?')
    aa = url[ind1 + 1:]
    bb = aa.split('&')
    for cc in bb:
        ind2 = cc.index('=')
        if ind2 > 0:
            key = cc[:ind2]
            val = cc[ind2 + 1:]
            query[key] = val
    return query


def _enc(x: str):
    return urllib.parse.quote(x)

default_base_url = os.getenv('FIGURL_BASE_URL', 'https://figurl.org')