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
    response = requests.post(url, data=payload)
    return response

def send_telegram_file(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    files = {
        'document': open(file_path, 'rb')
    }
    data = {
        'chat_id': CHAT_ID
    }
    response = requests.post(url, files=files, data=data)
    return response

# Step 1: 获取新的 API 数据
api_url = "https://monitor.gacjie.cn/api/client/get_ip_address?cdn_server=3"
response = requests.get(api_url)

# 调试：输出完整响应内容以查看结构
print(f"API Response: {response.text}")

if response.status_code == 200:
    try:
        # 从 JSON 响应中提取 "ip" 字段
        data = response.json()
        print(f"API JSON Data: {data}")  # 输出 JSON 数据，帮助调试
        ip_address = data.get('ip')  # 尝试获取 'ip' 字段

        if not ip_address:
            error_message = "未能提取到 IP 地址"
            send_telegram_message(error_message)
            raise Exception(error_message)
    except ValueError:
        # 如果无法解析 JSON，捕获异常并记录错误信息
        error_message = "API 响应不是有效的 JSON 格式"
        send_telegram_message(error_message)
        raise Exception(error_message)
else:
    error_message = f"API 请求失败，状态码: {response.status_code}"
    send_telegram_message(error_message)
    raise Exception(error_message)

# Step 2: 添加后缀
suffix = ":2053#Free"
processed_data = ip_address + suffix

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
