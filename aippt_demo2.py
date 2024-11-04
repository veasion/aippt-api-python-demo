import os
import time
from api import *


if __name__ == '__main__':
    # 根据主题异步流式生成PPT
    
    # 官网 https://docmee.cn
    # 开放平台 https://docmee.cn/open-platform/api
    
    # 填写你的API-KEY
    api_key = 'YOUR API KEY'
    
    # 第三方用户ID（数据隔离）
    uid = 'test'
    subject = 'AI未来的发展'
    
    # 创建 api token (有效期2小时，建议缓存到redis，同一个 uid 创建时之前的 token 会在10秒内失效)
    api_token = create_api_token(api_key, uid, None)
    print(f'apiToken: {api_token}')
    
    # 生成大纲
    print('\n\n========== 正在生成大纲 ==========')
    outline = generate_outline(api_token, subject, None, None)
    
    # 生成大纲内容同时异步生成PPT
    print('\n\n========== 正在异步生成大纲内容 ==========')
    pptInfo = async_generate_content(api_token, outline, None, None, None)
    
    ppt_id = pptInfo['id']
    print(f"pptId: {ppt_id}")
    
    # 下载PPT
    print('\n\n========== 正在下载PPT ==========')
    count = 0
    while count < 30:
        # 等待PPT文件可下载
        pptInfo = download_pptx(api_token, ppt_id)
        if pptInfo and 'fileUrl' in pptInfo and pptInfo['fileUrl']:
            break
        count = count + 1
        time.sleep(1)
    url = pptInfo['fileUrl']
    save_path = os.getcwd() + f'/{ppt_id}.pptx'
    print(f'ppt链接: {url}')
    download(url, save_path)
    print('ppt下载完成，保存路径：' + save_path)
 