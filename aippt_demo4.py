import os
from api import *


if __name__ == '__main__':
    # 通过文件直接生成 PPT
    
    # 官网 https://docmee.cn
    # 开放平台 https://docmee.cn/open-platform/api
    
    # 填写你的API-KEY
    api_key = 'YOUR API KEY'
    
    # 第三方用户ID（数据隔离）
    uid = 'test'
    # 文档文件，支持 word/excel/ppt/md/txt/pdf 等类型
    file_path = os.getcwd() + '/README.md'
    
    # 创建 api token (有效期2小时，建议缓存到redis，同一个 uid 创建时之前的 token 会在10秒内失效)
    api_token = create_api_token(api_key, uid, None)
    print(f'api token: {api_token}')
    
    # 解析文件
    data_url = parse_file_data(api_token, file_path, None, None)
    
    # 通过文件直接生成PPT
    print('\n正在生成PPT...\n')
    ppt_info = direct_generate_pptx(api_token, True, None, None, None, data_url)
    
    ppt_id = ppt_info['id']
    file_url = ppt_info['fileUrl']
    print("\n\n==============")
    print(f"pptId: {ppt_id}")
    print(f"ppt主题: {ppt_info['subject']}")
    print(f"ppt封面: {ppt_info['coverUrl']}")
    print(f"ppt链接: {file_url}")
    
    # 下载PPT
    save_path = os.getcwd() + f'/{ppt_id}.pptx'
    download(file_url, save_path)
    print('ppt下载完成，保存路径：' + save_path)
 