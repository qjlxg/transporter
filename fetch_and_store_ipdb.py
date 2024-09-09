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

# Step 1: 获取API数据
api_url = "https://ipdb.api.030101.xyz/?type=bestcf"
response = requests.get(api_url)
if response.status_code == 200:
    data = response.text
else:
    error_message = f"API 请求失败，状态码: {response.status_code}"
    send_telegram_message(error_message)
    raise Exception(error_message)

# Step 2: 添加后缀
suffix = ":2053#Free"
processed_data = "\n".join([line + suffix for line in data.splitlines()])

# Step 3: 将数据保存为固定名称的文件
filename = "ipdb_data.txt"
file_path = os.path.join("data", filename)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

# 覆写文件（直接写入新内容）
with open(file_path, "w") as file:
    file.write(processed_data)

success_message = f"数据已保存"
send_telegram_message(success_message)
send_telegram_file(file_path)

print(success_message)

# Step 4: 将文件提交到GitHub仓库
os.system("git add data/")
os.system('git commit -m "Add new IPDB data with suffix" || echo "No changes to commit"')
os.system("git pull origin main --rebase || git rebase --abort")
os.system("git push origin main")
