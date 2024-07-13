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


def handle_stream_data(json: any, ppt_info: list):
    if 'status' in json and json['status'] == -1:
        raise RuntimeError('请求异常：' + json['error'])
    if 'result' in json and json['status'] == 4:
        ppt_info.append(json['result'])
    print(json['text'], end='')


def direct_generate_pptx(api_token: str, stream: bool, template_id: str, subject: str, pptx_property=False, prompt=None, data_url=None) -> any:
    url = BASE_URL + '/ppt/directGeneratePptx'
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
        response = post_sse(url, { 'token': api_token }, body, lambda json: handle_stream_data(json, ppt_info), True)
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


if __name__ == '__main__':
    # 直接生成 PPT
    
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
    
    # 通过主题直接生成PPT
    print('\n正在生成PPT...\n')
    ppt_info = direct_generate_pptx(api_token, True, None, subject)
    
    ppt_id = ppt_info['id']
    file_url = ppt_info['fileUrl']
    print("\n\n==============")
    print(f"pptId: {ppt_id}")
    print(f"ppt主题: {ppt_info['subject']}")
    print(f"ppt封面: {ppt_info['coverUrl']}?token={api_token}")
    print(f"ppt链接: {file_url}")
    
    # 下载PPT
    save_path = os.getcwd() + f'/{ppt_id}.pptx'
    download(file_url, save_path)
    print('ppt下载完成，保存路径：' + save_path)
 