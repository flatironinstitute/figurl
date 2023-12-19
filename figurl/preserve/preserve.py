from typing import Any, List
import os
import tempfile
import json
import shutil
import kachery_cloud as kcl


def preserve(*, figurl_url: str, output_folder: str):
    if os.path.exists(output_folder):
        raise Exception(f'Output folder already exists: {output_folder}')
    os.mkdir(output_folder)
    view_uri, data_uri, label = _parse_figurl_url(figurl_url)
    if not view_uri.startswith('npm://'):
        raise Exception('View must be of the form npm://...')
    view_folder = os.path.join(output_folder, 'view')
    os.mkdir(view_folder)
    _copy_npm_site_to_folder(view_uri, view_folder)
    _patch_index_html(os.path.join(view_folder, 'index.html'))
    data_folder = os.path.join(output_folder, 'data')
    os.mkdir(data_folder)
    data_index_json_path = os.path.join(data_folder, 'index.json')
    kcl.load_file(data_uri, dest=data_index_json_path)
    with open(data_index_json_path, 'r') as f:
        data_index = json.load(f)
    _load_sha1_files_from_object(object=data_index, data_folder=data_folder)
    thisdir = os.path.dirname(os.path.realpath(__file__))
    _copy_template_files_to_folder(templates_folder=os.path.join(thisdir, 'templates'), output_folder=output_folder)

def _copy_npm_site_to_folder(npm_uri: str, folder: str):
    package_name, path = _parse_npm_uri(npm_uri)
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f'npm pack {package_name} --pack-destination {tmpdir}')
        os.system(f'tar -xvf {tmpdir}/*.tgz -C {tmpdir}')
        os.system(f'cp -r {tmpdir}/package/{path}/* {folder}/')

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

def _patch_index_html(path: str):
    with open(path, 'r') as f:
        txt = f.read()
    txt = txt.replace('<head>', '<head><base href="view/">')
    with open(path, 'w') as f:
        f.write(txt)
