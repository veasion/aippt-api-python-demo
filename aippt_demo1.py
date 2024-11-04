import os
from api import *


if __name__ == '__main__':
    # 同步流式生成 PPT
    
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
    
    # 生成大纲内容
    print('\n\n========== 正在生成大纲内容 ==========')
    markdown = generate_content(api_token, outline, None, None)
    
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
    pptInfo = download_pptx(api_token, ppt_id)
    url = pptInfo['fileUrl']
    save_path = os.getcwd() + f'/{ppt_id}.pptx'
    print(f'ppt链接: {url}')
    download(url, save_path)
    print('ppt下载完成，保存路径：' + save_path)
 