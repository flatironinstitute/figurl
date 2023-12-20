from typing import Any, List
import os
import tempfile
import json
import shutil
import requests
import kachery_cloud as kcl


def preserve_figure(*, figurl_url: str, output_file: str):
    if not output_file.endswith('.tar.gz') and not output_file.endswith('.tgz'):
        raise Exception('Output file must end with .tar.gz or .tgz')
    if os.path.exists(output_file):
        raise Exception(f'Output file already exists: {output_file}')
    view_uri, data_uri, label = _parse_figurl_url(figurl_url)
    view_url = _view_uri_to_url(view_uri)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_output_folder = os.path.join(tmpdir, 'figure')
        os.mkdir(tmp_output_folder)
        view_folder = os.path.join(tmp_output_folder, 'view')
        os.mkdir(view_folder)
        _copy_site_to_folder(view_url, view_folder)
        data_folder = os.path.join(tmp_output_folder, 'data')
        os.mkdir(data_folder)
        data_index_json_path = os.path.join(data_folder, 'index.json')
        kcl.load_file(data_uri, dest=data_index_json_path)
        with open(data_index_json_path, 'r') as f:
            data_index = json.load(f)
        _load_sha1_files_from_object(object=data_index, data_folder=data_folder)
        thisdir = os.path.dirname(os.path.realpath(__file__))
        _copy_template_files_to_folder(templates_folder=os.path.join(thisdir, 'templates'), output_folder=tmp_output_folder)
        os.system(f'tar -czvf {output_file} -C {tmpdir} figure')

def _copy_site_to_folder(site_url: str, folder: str):
    manifest_url = site_url + '/file-manifest.txt'
    try:
        file_manifest_txt = _download_file_text(manifest_url)
    except:
        print(f'Problem downloading manifest file: {manifest_url}')
        print(f'Perhaps this view does not have a file-manifest.txt file.')
        raise Exception('Unable to download file-manifest.txt')
    file_list = file_manifest_txt.split('\n')
    for f in file_list:
        a = f.split('/')
        for i in range(len(a) - 1):
            dirpath = os.path.join(folder, *a[0:i + 1])
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
        url = site_url + '/' + f
        _download_file(url, os.path.join(folder, f))

def _download_file_text(url: str):
    print(f'Downloading file: {url}')
    r = requests.get(url)
    if not r.ok:
        raise Exception(f'Problem downloading file: {url}')
    return r.text

def _download_file(url: str, dest: str):
    print(f'Downloading file: {url}')
    r = requests.get(url)
    if not r.ok:
        raise Exception(f'Problem downloading file: {url}')
    # stream file to disk
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def _parse_npm_uri(npm_uri: str):
    a = npm_uri.split('/')
    if a[0] != 'npm:':
        raise Exception(f'Invalid npm uri: {npm_uri}')
    if a[1] != '':
        raise Exception(f'Invalid npm uri: {npm_uri}')
    if a[2].startswith('@'):
        package_name = a[2] + '/' + a[3]
        path = '/'.join(a[4:])
    else:
        package_name = a[2]
        path = '/'.join(a[3:])
    return package_name, path

def _parse_figurl_url(url: str):
    ind_q = url.find('?')
    if ind_q < 0:
        raise Exception('Invalid figurl url: missing ?')
    query = url[ind_q + 1:]
    view_uri = None
    data_uri = None
    label = None
    for item in query.split('&'):
        if item.startswith('v='):
            view_uri = item[len('v='):]
        elif item.startswith('d='):
            data_uri = item[len('d='):]
        elif item.startswith('label='):
            label = item[len('label='):]
        else:
            pass
    if view_uri is None:
        raise Exception('Invalid figurl url: missing view uri')
    if data_uri is None:
        raise Exception('Invalid figurl url: missing data uri')
    if label is None:
        label = ''
    return view_uri, data_uri, label

def _load_sha1_files_from_object(*, object: Any, data_folder: str):
    sha1_uris = _get_sha1_uris_from_object(object)
    sha1s = []
    for uri in sha1_uris:
        try:
            sha1 = uri.split('/')[2].split('?')[0]
        except:
            print(f'Warning: problem parsing uri: {uri}')
            sha1 = None
        if sha1 is not None:
            sha1s.append(sha1)
    for sha1 in sha1s:
        if not os.path.exists(os.path.join(data_folder, 'sha1')):
            os.mkdir(os.path.join(data_folder, 'sha1'))
        kcl.load_file(f'sha1://{sha1}', dest=os.path.join(data_folder, 'sha1', sha1))

def _get_sha1_uris_from_object(object: Any):
    if isinstance(object, str):
        if object.startswith('sha1://'):
            return [object]
        else:
            return []
    elif isinstance(object, dict):
        ret: List[str] = []
        for key in object.keys():
            ret.extend(_get_sha1_uris_from_object(object[key]))
        return ret
    elif isinstance(object, list):
        ret: List[str] = []
        for item in object:
            ret.extend(_get_sha1_uris_from_object(item))
        return ret
    else:
        return []

def _copy_template_files_to_folder(*, templates_folder: str, output_folder: str):
    for f in os.listdir(templates_folder):
        # check if directory
        if os.path.isdir(os.path.join(templates_folder, f)):
            shutil.copytree(os.path.join(templates_folder, f), os.path.join(output_folder, f))
        else:
            shutil.copy(os.path.join(templates_folder, f), os.path.join(output_folder, f))

def _view_uri_to_url(uri: str):
    if uri.startswith('npm://'):
        package_name, path = _parse_npm_uri(uri)
        return f'https://unpkg.com/{package_name}/{path}'