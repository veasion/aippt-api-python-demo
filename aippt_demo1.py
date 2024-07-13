import json, os
from http_utils import *

BASE_URL = 'https://chatmee.cn/api'


def create_api_token(api_key: str, uid: str) -> str:
    url = BASE_URL + '/user/createApiToken'
    body = json.dumps({ 'uid': uid })
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
    url = BASE_URL + '/ppt/generateOutline'
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
    url = BASE_URL + '/ppt/generateContent'
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
    url = BASE_URL + '/ppt/randomTemplates'
    body = json.dumps({ 'size': 1, 'filters': { 'type': 1 } })
    response = post_json(url, { 'token': api_token }, body)
    if response.status_code != 200:
        raise RuntimeError('获取模板失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('获取模板异常：' + result['message'])
    return result['data'][0]['id']


def generate_pptx(api_token: str, template_id: str, markdown: str, pptx_property=False) -> any:
    url = BASE_URL + '/ppt/generatePptx'
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
    url = BASE_URL + '/ppt/downloadPptx'
    body = json.dumps({ 'id': id })
    response = post_json(url, { 'token': api_token }, body)
    if response.status_code != 200:
        raise RuntimeError('下载PPT失败，httpStatus=' + str(response.status_code))
    result = json.loads(response.text)
    if result['code'] != 0:
        raise RuntimeError('下载PPT异常：' + result['message'])
    return result['data']['fileUrl']


if __name__ == '__main__':
    # 流式生成 PPT
    
    # 官网 https://docmee.cn
    # 开放平台 https://docmee.cn/open-platform/api
    
    # 填写你的API-KEY
    api_key = '{ YOUR API KEY }'
    
    # 第三方用户ID（数据隔离）
    uid = 'test'
    subject = 'AI未来的发展'
    
    # 创建 apiToken (有效期2小时，建议缓存到redis)
    api_token = create_api_token(api_key, uid)
    print(f'apiToken: {api_token}')
    
    # 生成大纲
    print('\n\n========== 正在生成大纲 ==========')
    outline = generate_outline(api_token, subject)
    
    # 生成大纲内容
    print('\n\n========== 正在生成大纲内容 ==========')
    markdown = generate_content(api_token, outline)
    
    # 随机一个模板
    print('\n\n========== 随机选择模板 ==========')
    template_id = random_one_template_id(api_token)
    print(f'templateId: {template_id}')
    
    # 生成PPT
    print('\n\n========== 正在生成PPT ==========')
    ppt_info = generate_pptx(api_token, template_id, markdown)
    
    ppt_id = ppt_info['id']
    print(f"pptId: {ppt_id}")
    print(f"ppt主题: {ppt_info['subject']}")
    print(f"ppt封面: {ppt_info['coverUrl']}?token={api_token}")
    
    # 下载PPT
    print('\n\n========== 正在下载PPT ==========')
    url = download_pptx(api_token, ppt_id)
    save_path = os.getcwd() + f'/{ppt_id}.pptx'
    print(f'ppt链接: {url}')
    download(url, save_path)
    print('ppt下载完成，保存路径：' + save_path)
 
