import requests
from bs4 import BeautifulSoup
import base64

# 目标网址
url = 'https://jc.guanxi.cloudns.be/'

def fetch_subscription_links(url, keywords_to_remove, keywords_to_filter_lines):
    # 发送 HTTP 请求
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设定编码，避免乱码

    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 筛选包含 "长按复制订阅链接" 的内容
        target_texts = soup.find_all(string=lambda text: "订阅链接" in text)
        
        # 保存订阅链接
        with open("data/gx.txt", "w", encoding="utf-8") as file:
            for target in target_texts:
                parent = target.find_parent()  # 获取包含目标文本的父元素
                if parent:
                    # 查找链接
                    links = parent.find_all('a', href=True)
                    for link in links:
                        try:
                            href = link.get('href')
                            
                            # Base64 解码
                            response = requests.get(href)
                            response.encoding = 'utf-8'
                            decoded_content = base64.b64decode(response.text).decode('utf-8')
                            
                            # 删除指定关键词
                            for keyword in keywords_to_remove:
                                decoded_content = decoded_content.replace(keyword, '')

                            # 按行过滤包含指定关键词的行
                            filtered_lines = [
                                line for line in decoded_content.splitlines()
                                if not any(keyword in line for keyword in keywords_to_filter_lines)
                            ]

                            # 合并处理后的内容
                            filtered_content = '\n'.join(filtered_lines)

                            # Base64 重新编码
                            encoded_content = base64.b64encode(filtered_content.encode('utf-8')).decode('utf-8')

                            # 写入到文件
                            file.write(encoded_content + '\n')

                        except requests.RequestException as e:
                            file.write(f"Failed to retrieve {href}: {e}\n\n")
                        except Exception as e:
                            file.write(f"Error processing {href}: {e}\n\n")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 指定要删除的关键词
keywords_to_remove = ["关键词1", "关键词2"]

# 指定要过滤整行的关键词
keywords_to_filter_lines = ["关注", "频道", ""]
print(soup.prettify())  
# 输出完整的 HTML，确认内容是否加载
# 执行函数
fetch_subscription_links(url, keywords_to_remove, keywords_to_filter_lines)
