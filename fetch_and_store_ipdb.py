import requests
import os

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = '7105513269:AAGxdsjP9P6cp3wPdZeeLqmSA7wiBxn5ll8'  # 替换为你的 Telegram Bot Token
CHAT_ID = '-1002242550802'  # 替换为你的 Chat ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def send_telegram_file(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    files = {
        'document': open(file_path, 'rb')
    }
    data = {
        'chat_id': CHAT_ID
    }
    requests.post(url, files=files, data=data)

def fetch_ips_from_api(api_url):
    response = requests.get(api_url)
    ip_addresses = []

    if response.status_code == 200:
        try:
            data = response.json()
            info = data.get('info', {})

            # 提取 CM、CU、CT 的 IP 地址
            for group in ['CM', 'CU', 'CT']:
                for entry in info.get(group, []):
                    ip = entry.get('ip')
                    if ip:
                        ip_addresses.append(ip)
        except ValueError:
            send_telegram_message(f"API 响应不是有效的 JSON 格式: {api_url}")
    else:
        send_telegram_message(f"API 请求失败，状态码: {response.status_code}，地址: {api_url}")

    return ip_addresses

# 设定 API 列表
api_urls = [
    "https://monitor.gacjie.cn/api/client/get_ip_address?cdn_server=3",
    "https://raw.githubusercontent.com/BruceWind/GcoreCDNIPSelector/refs/heads/main/result.txt",  # 另一个 API 示例
    # 可以添加更多 API
]

# 从所有 API 提取 IP
all_ips = []
for url in api_urls:
    all_ips.extend(fetch_ips_from_api(url))

if not all_ips:
    send_telegram_message("未能提取到任何 IP 地址")
    raise Exception("未能提取到任何 IP 地址")

# Step 2: 添加后缀
suffix = ":2053#Free"
processed_data = "\n".join([ip + suffix for ip in all_ips])

# Step 3: 将数据保存为固定名称的文件
filename = "ipdb_data.txt"
file_path = os.path.join("data", filename)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

# 覆写文件（直接写入新内容）
with open(file_path, "w") as file:
    file.write(processed_data)

success_message = "数据已保存"
send_telegram_message(success_message)
send_telegram_file(file_path)

print(success_message)

# Step 4: 将文件提交到GitHub仓库
os.system("git add data/")
os.system('git commit -m "Add new IPDB data with suffix" || echo "No changes to commit"')
os.system("git pull origin main --rebase || git rebase --abort")
os.system("git push origin main")
