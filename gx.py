import requests
from bs4 import BeautifulSoup
import base64

# 目标网址
url = 'https://jc.guanxi.cloudns.be/'

def fetch_api_links_content(url, keywords_to_remove, keywords_to_filter_lines):
    # 发送 HTTP 请求
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设定编码，避免乱码

    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 筛选并保留包含 'token' 的链接
        api_links = [a.get('href') for a in soup.find_all('a', href=True) if 'token' in a.get('href')]

        # 如果没有找到符合条件的链接
        if not api_links:
            print("未找到符合条件的链接。")
            return

        # 打开文件进行写入
        with open("data/gx.txt", "w", encoding="utf-8") as file:
            for link in api_links:
                try:
                    print(f"正在处理链接: {link}")

                    # 获取 API 链接内容
                    api_response = requests.get(link)
                    api_response.encoding = 'utf-8'
                    
                    # 打印返回内容的前100字符（用于调试）
                    print("API 返回内容（前100字符）:", api_response.text)  

                    # Base64 解码
                    try:
                        decoded_content = base64.b64decode(api_response.text).decode('utf-8')
                    except Exception as e:
                        print(f"Base64 解码失败: {e}")
                        continue  # 如果解码失败，跳过此链接

                    # 打印解码后的内容（用于调试）
                    print("解码后的内容:", decoded_content)  # 打印前100字符

                    # 删除指定的关键词
                    for keyword in keywords_to_remove:
                        decoded_content = decoded_content.replace(keyword, '')

                    # 过滤包含指定关键词的行
                    filtered_lines = [line for line in decoded_content.splitlines() 
                                      if not any(keyword in line for keyword in keywords_to_filter_lines)]

                    # 合并处理后的内容
                    filtered_content = '\n'.join(filtered_lines)

                    # 打印过滤后的内容（用于调试）
                    print("过滤后的内容:", filtered_content)  # 打印前100字符

                    # Base64 重新编码
                    encoded_content = base64.b64encode(filtered_content.encode('utf-8')).decode('utf-8')

                    # 写入文件
                    file.write(encoded_content + '\n')

                except requests.RequestException as e:
                    print(f"请求失败: {link} - 错误: {e}")
                except Exception as e:
                    print(f"处理链接时出错: {link} - 错误: {e}")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 指定要删除的关键词
keywords_to_remove = ["%40MFJD666", "关键词2"]

# 指定要过滤的整行关键词
keywords_to_filter_lines = ["%E5%86%A0%E5%B8%8C", "%E9%A2%91%E9%81%93","%E5%85%B3%E6%B3%A8"]

# 执行函数
fetch_api_links_content(url, keywords_to_remove, keywords_to_filter_lines)
