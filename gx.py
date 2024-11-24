import requests
from bs4 import BeautifulSoup
import base64

# 目标网址
url = 'https://jc.guanxi.cloudns.be/'

# 指定要删除的关键词
keywords_to_remove = ["敏感词1", "敏感词2"]  # 替换为实际关键词

def fetch_api_links_content(url):
    # 发送 HTTP 请求
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设定编码，避免乱码

    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 筛选并保留包含 'api' 的链接
        api_links = [a.get('href') for a in soup.find_all('a', href=True) if 'api' in a.get('href')]
        
        # 获取每个 API 链接的内容并保存
        with open("data/gx.txt", "w", encoding="utf-8") as file:
            for link in api_links:
                try:
                    # 获取 API 链接内容
                    api_response = requests.get(link)
                    api_response.encoding = 'utf-8'

                    # Base64 解码
                    decoded_content = base64.b64decode(api_response.text).decode('utf-8')

                    # 删除指定关键词
                    for keyword in keywords_to_remove:
                        decoded_content = decoded_content.replace(keyword, "")

                    # Base64 再次加密
                    encoded_content = base64.b64encode(decoded_content.encode('utf-8')).decode('utf-8')

                    # 写入到文件
                    file.write(encoded_content + "\n")
                
                except (requests.RequestException, base64.binascii.Error, UnicodeDecodeError) as e:
                    file.write(f"Failed to process {link}: {e}\n\n")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 执行函数
fetch_api_links_content(url)
