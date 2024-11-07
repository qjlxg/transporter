import requests
from bs4 import BeautifulSoup

# 目标网址
url = 'https://jc.guanxi.cloudns.be/'

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
                    api_response = requests.get(link)
                    api_response.encoding = 'utf-8'
                    file.write(f"URL: {link}\n")
                    file.write(api_response.text)
                    file.write("\n\n" + "="*50 + "\n\n")  # 分隔不同链接内容
                except requests.RequestException as e:
                    file.write(f"Failed to retrieve {link}: {e}\n\n")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 执行函数
fetch_api_links_content(url)
