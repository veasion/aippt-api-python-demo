import requests, json


def post_sse(url: str, headers: any, body: str, consumer, to_json=False) -> requests.Response:
    if not headers:
        headers = {}
    headers['Content-Type'] = 'application/json'
    response = requests.post(url, headers=headers, data=body, stream=True, verify=False)
    if response.status_code == 200:
        for line in response.iter_lines():
            str = line.decode('utf-8')
            if str.startswith('data:'):
                str = str[6 if str.startswith('data: ') else 5:]
                if str == '' or str == '[DONE]':
                    continue
                if to_json:
                    consumer(json.loads(str))
                else:
                    consumer(str)
    return response


def post_json(url: str, headers: any, body: str) -> requests.Response:
    if not headers:
        headers = {}
    headers['Content-Type'] = 'application/json'
    return requests.post(url, headers=headers, data=body, verify=False)


def download(url: str, save_path: str):
    file = requests.get(url, verify=False)
    with open(save_path, 'wb') as wstream:
        wstream.write(file.content)
