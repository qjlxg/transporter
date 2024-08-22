import requests
from datetime import datetime
import os

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'  # 替换为你的 Telegram Bot Token
CHAT_ID = 'your_chat_id'  # 替换为你的 Chat ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response

# Step 1: 获取API数据
api_url = "https://ipdb.api.030101.xyz/?type=bestcf&country=true"
response = requests.get(api_url)
if response.status_code == 200:
    data = response.text
else:
    error_message = f"API 请求失败，状态码: {response.status_code}"
    send_telegram_message(error_message)
    raise Exception(error_message)

# Step 2: 将数据保存为文件
filename = f"ipdb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
file_path = os.path.join("data", filename)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

# 删除旧文件（如果存在）
for file in os.listdir("data"):
    if file.endswith(".txt"):
        os.remove(os.path.join("data", file))

# 创建新文件
with open(file_path, "w") as file:
    file.write(data)

success_message = f"数据已保存到 {file_path}"
send_telegram_message(success_message)

print(success_message)

# Step 3: 将文件提交到GitHub仓库
os.system("git add data/")
os.system(f'git commit -m "Add new IPDB data"')
os.system("git pull origin main --rebase")  # 确保最新的远程更改合并到本地
os.system("git push origin main")
