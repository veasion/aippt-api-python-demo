import json
from http_utils import *

BASE_URL = 'https://chatmee.cn'


def create_api_token(api_key: str, uid: str, limit: int|None) -> str:
    url = BASE_URL + '/api/user/createApiToken'
    body = json.dumps({ 'uid': uid, 'limit': limit })
    response = post_json(url, { 'Api-Key': api_key }, body)
    if response.status_code != 200:
        raise RuntimeError('创建apiToken失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('创建apiToken异常：' + result['message'])
    return result['data']['token']


def handle_stream_data(json: any, sb: list):
    if 'status' in json and json['status'] == -1:
        raise RuntimeError('请求异常：' + json['error'])
    sb.append(json['text'])
    print(json['text'], end='')


def generate_outline(api_token: str, subject: str, prompt=None, data_url=None) -> str:
    url = BASE_URL + '/api/ppt/generateOutline'
    body = json.dumps({
        'subject': subject,
        'prompt': prompt,
        'dataUrl': data_url
    })
    sb = []
    response = post_sse(url, { 'token': api_token }, body, lambda json: handle_stream_data(json, sb), True)
    if response.status_code != 200:
        raise RuntimeError('生成大纲失败，httpStatus=' + str(response.status_code))
    if response.headers['Content-Type'] in 'application/json':
        result = json.loads(response.text)
        raise RuntimeError('生成大纲异常：' + result['message'])
    return ''.join(sb)


def generate_content(api_token: str, outline: str, prompt=None, data_url=None) -> str:
    url = BASE_URL + '/api/ppt/generateContent'
    body = json.dumps({
        'outlineMarkdown': outline,
        'prompt': prompt,
        'dataUrl': data_url
    })
    sb = []
    response = post_sse(url, { 'token': api_token }, body, lambda json: handle_stream_data(json, sb), True)
    if response.status_code != 200:
        raise RuntimeError('生成大纲内容，httpStatus=' + str(response.status_code))
    if response.headers['Content-Type'] in 'application/json':
        result = json.loads(response.text)
        raise RuntimeError('生成大纲内容异常：' + result['message'])
    return ''.join(sb)


def random_one_template_id(api_token: str) -> str:
    url = BASE_URL + '/api/ppt/randomTemplates'
    body = json.dumps({ 'size': 1, 'filters': { 'type': 1 } })
    response = post_json(url, { 'token': api_token }, body)
    if response.status_code != 200:
        raise RuntimeError('获取模板失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('获取模板异常：' + result['message'])
    return result['data'][0]['id']


def generate_pptx(api_token: str, template_id: str, markdown: str, pptx_property=False) -> any:
    url = BASE_URL + '/api/ppt/generatePptx'
    body = json.dumps({
        'templateId': template_id,
        'outlineContentMarkdown': markdown,
        'pptxProperty': pptx_property
    })
    response = post_json(url, { 'token': api_token }, body)
    if response.status_code != 200:
        raise RuntimeError('生成PPT失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('生成PPT异常：' + result['message'])
    return result['data']['pptInfo']


def download_pptx(api_token: str, id: str) -> str:
    url = BASE_URL + '/api/ppt/downloadPptx'
    body = json.dumps({ 'id': id })
    response = post_json(url, { 'token': api_token }, body)
    if response.status_code != 200:
        raise RuntimeError('下载PPT失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('下载PPT异常：' + result['message'])
    return result['data']['fileUrl']


def handle_direct_stream_data(json: any, ppt_info: list):
    if 'status' in json and json['status'] == -1:
        raise RuntimeError('请求异常：' + json['error'])
    if 'result' in json and json['status'] == 4:
        ppt_info.append(json['result'])
    print(json['text'], end='')


def direct_generate_pptx(api_token: str, stream: bool, template_id: str, subject: str, pptx_property=False, prompt=None, data_url=None) -> any:
    url = BASE_URL + '/api/ppt/directGeneratePptx'
    body = json.dumps({
        'stream': stream,
        'templateId': template_id,
        'subject': subject,
        'prompt': prompt,
        'dataUrl': data_url,
        'pptxProperty': pptx_property
    })
    if stream:
        ppt_info = []
        response = post_sse(url, { 'token': api_token }, body, lambda json: handle_direct_stream_data(json, ppt_info), True)
        if response.status_code != 200:
            raise RuntimeError('生成PPT，httpStatus=' + str(response.status_code))
        if response.headers['Content-Type'] in 'application/json':
            result = json.loads(response.text)
            raise RuntimeError('生成PPT异常：' + result['message'])
        return ppt_info[0]
    else:
        response = post_json(url, { 'token': api_token }, body)
        if response.status_code != 200:
            raise RuntimeError('生成PPT，httpStatus=' + str(response.status_code))
        result = json.loads(response.text)
        if result['code'] != 0:
            raise RuntimeError('生成PPT异常：' + result['message'])
        return result['data']['pptInfo']
