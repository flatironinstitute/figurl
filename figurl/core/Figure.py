import os
import subprocess
import json
from typing import Any, Union
import urllib.parse
import kachery_cloud as kcl
from .serialize_wrapper import _serialize

class Figure:
    def __init__(self, *, data: Any, view_url: Union[str, None]=None, access_group: Union[str, None]=None):
        self._view_url = view_url
        self._data = data
        self._serialized_data = _serialize(self._data, compress_npy=True)
        self._access_group = access_group

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
    def set_data(self, data: Any):
        self._data = data
        self._serialized_data = _serialize(data, compress_npy=True)
    def url(self, *, label: str, project_id: Union[str, None]=None, base_url: Union[str, None]=None, view_url: Union[str, None] = None, hide_app_bar: bool=False, local: bool=False):
        if base_url is None:
            base_url = default_base_url
        if self._view_url is not None: # new system:
            # if self._data_uri is None:
            #     self._data_uri = kc.store_json(self._serialized_data)
            # data_hash = self._data_uri.split('/')[2]
            # kc.upload_file(self._data_uri, channel=channel, single_chunk=True)
            self._data_uri = kcl.store_json(self._serialized_data, local=local)
            if self._access_group is not None:
                self._data_uri = kcl.encrypt_uri(self._data_uri, access_group=self._access_group)
            data_uri = self._data_uri
            if view_url is None:
                view_url = self._view_url
            url = f'{base_url}/f?v={view_url}&d={data_uri}'
            if project_id is not None:
                url += f'&project={project_id}'
            if hide_app_bar:
                url += '&hide=1'
            url += f'&label={_enc(label)}'
            if local:
                url += '&local=1'
            return url
        else:
            raise Exception('No self._view_url')
    def electron(self, *, label: str, listen_port: Union[int, None]=None):
        url = self.url(label=label, local=True) # important to use local
        query = _parse_url(url)
        vv = query['v']
        dd = query['d']
        label = query.get('label', '')
        cmd = f'figurl-electron -d {dd} -v {vv}'
        if label:
            cmd = cmd + f' --label {label}'
        if listen_port is not None:
            cmd = cmd + f' --listenPort {listen_port}'

        # this is important because $HOME sometimes gets remapped with electron
        env = os.environ.copy()
        env["KACHERY_CLOUD_DIR"] = kcl.get_kachery_cloud_dir()

        # retcode = subprocess.run(cmd.split(' '), env=env, check=True).returncode
        # if retcode != 0:
        #     print('Error running electron app. Is figurl-electron installed?')
        subprocess.Popen(cmd.split(' '), env=env)

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