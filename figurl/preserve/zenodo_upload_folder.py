import os
import requests


# Maybe at some point we'll want to do this. But for now there is no use case for it.

def zenodo_upload_folder(*,
    source_folder: str,
    record_id: str,
    sandbox: bool,
    dest: str
):
    if sandbox:
        API_TOKEN = os.environ.get('ZENODO_SANDBOX_API_TOKEN', None)
        if not API_TOKEN:
            raise Exception('Missing ZENODO_SANDBOX_API_TOKEN environment variable')
    else:
        API_TOKEN = os.environ.get('ZENODO_API_TOKEN', None)
        if not API_TOKEN:
            raise Exception('Missing ZENODO_API_TOKEN environment variable')
    all_files_relpaths = _get_all_files_relpaths(source_folder)
    if len(all_files_relpaths) > 200:
        raise Exception('Too many files')
    for f in all_files_relpaths:
        size = os.path.getsize(os.path.join(source_folder, f))
        if size > 1024 * 1024 * 1024:
            raise Exception(f'File is too large: {f}')
    for f in all_files_relpaths:
        _upload_file(
            source_folder=source_folder,
            relpath=f,
            record_id=record_id,
            sandbox=sandbox,
            dest=dest,
            API_TOKEN=API_TOKEN
        )

def _upload_file(*,
    source_folder: str,
    relpath: str,
    record_id: str,
    sandbox: bool,
    dest: str,
    API_TOKEN: str
):
    print(f'Uploading file: {relpath}')
    base_url = 'https://sandbox.zenodo.org' if sandbox else 'https://zenodo.org'

    dest_file_path = relpath if dest == '.' or dest == '' else os.path.join(dest, relpath)
    
    # create file with a POST request
    url = f'{base_url}/api/records/{record_id}/draft/files'
    url += f'?access_token={API_TOKEN}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = [
        {
            'key': dest_file_path
        }
    ]
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        raise Exception(f'Problem creating file: {response.status_code} {response.reason}')

    # upload file content with a PUT request
    url = f'{base_url}/api/records/{record_id}/draft/files/{dest_file_path}/content'
    url += f'?access_token={API_TOKEN}'
    headers = {
        'Content-Type': 'application/octet-stream'
    }
    with open(os.path.join(source_folder, relpath), 'rb') as f:
        data = f.read()
    response = requests.put(url, headers=headers, data=data)
    if not response.ok:
        raise Exception(f'Problem uploading file content: {response.status_code} {response.reason}')
    
    # commit file with a POST request
    url = f'{base_url}/api/records/{record_id}/draft/files/{dest_file_path}/commit'
    url += f'?access_token={API_TOKEN}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {}
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        raise Exception(f'Problem committing file: {response.status_code} {response.reason}')

def _get_all_files_relpaths(source_folder: str):
    all_files_relpaths = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            relpath = os.path.relpath(os.path.join(root, file), source_folder)
            all_files_relpaths.append(relpath)
    return all_files_relpaths
