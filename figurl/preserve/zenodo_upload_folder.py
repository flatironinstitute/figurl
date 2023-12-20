import os
import requests


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

# curl 'https://sandbox.zenodo.org/api/records/11269/draft/files' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Type: application/json' \
#   -H 'Cookie: 04f20c86f07421a9ec0f9d5ba4be544f=7705ef0ecdb4f5b5c6800bf05b654082; _pk_ref.365.3783=%5B%22%22%2C%22%22%2C1702996065%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.365.3783=780b7fd43e8700f2.1702996065.; _pk_ses.365.3783=1; session=9ac56bc971221ab3_6581a868.5zCyz__CQpDwgQASBqnEbDrL6FY; csrftoken=eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'Origin: https://sandbox.zenodo.org' \
#   -H 'Referer: https://sandbox.zenodo.org/uploads/11269' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#   -H 'X-CSRFToken: eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Linux"' \
#   --data-raw '[{"key":"setup.py"}]' \
#   --compressed

# curl 'https://sandbox.zenodo.org/api/records/11269/draft/files/setup.py/content' \
#   -X 'PUT' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Length: 422' \
#   -H 'Content-Type: application/octet-stream' \
#   -H 'Cookie: 04f20c86f07421a9ec0f9d5ba4be544f=7705ef0ecdb4f5b5c6800bf05b654082; _pk_ref.365.3783=%5B%22%22%2C%22%22%2C1702996065%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.365.3783=780b7fd43e8700f2.1702996065.; _pk_ses.365.3783=1; session=9ac56bc971221ab3_6581a868.5zCyz__CQpDwgQASBqnEbDrL6FY; csrftoken=eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'Origin: https://sandbox.zenodo.org' \
#   -H 'Referer: https://sandbox.zenodo.org/uploads/11269' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#   -H 'X-CSRFToken: eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Linux"' \
#   --compressed

# curl 'https://sandbox.zenodo.org/api/records/11269/draft/files/setup.py/commit' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Type: application/json' \
#   -H 'Cookie: 04f20c86f07421a9ec0f9d5ba4be544f=7705ef0ecdb4f5b5c6800bf05b654082; _pk_ref.365.3783=%5B%22%22%2C%22%22%2C1702996065%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.365.3783=780b7fd43e8700f2.1702996065.; _pk_ses.365.3783=1; session=9ac56bc971221ab3_6581a868.5zCyz__CQpDwgQASBqnEbDrL6FY; csrftoken=eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'Origin: https://sandbox.zenodo.org' \
#   -H 'Referer: https://sandbox.zenodo.org/uploads/11269' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#   -H 'X-CSRFToken: eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMjk5NjA3MiwiZXhwIjoxNzAzMDgyNDcyfQ.IjVzdXhGdkZCcVlDYlJGVnJka2JROERmeFd1Vm0zNmNaIg.cw7nlIZ-cV3qvghFt6IuQaULZ-8s6gCu85zBee5OXJDRoSz179cMNd2LuoLB4Ic92EWR-Llt6H6xP_goU2AXsA' \
#   -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Linux"' \
#   --data-raw '{}' \
#   --compressed