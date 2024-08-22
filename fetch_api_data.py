import requests

# API URL
url = "https://ipdb.api.030101.xyz/?type=bestcf&country=true"

# Telegram Bot 配置
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'  # 替换为你的 Bot API 令牌
chat_id = 'YOUR_CHAT_ID'  # 替换为你的 Chat ID

# 需要添加的后缀
suffix = " #后缀"

# 发送请求获取API内容
response = requests.get(url)
data = response.text

# 为每一行添加后缀
modified_data = ""
for line in data.splitlines():
    modified_data += line + suffix + "\n"

# 将修改后的数据保存到文件
with open("api_data.txt", "w") as file:
    file.write(modified_data)

# 准备要发送到Telegram的消息
message = "API数据已更新并推送到GitHub仓库。"

# 发送消息到Telegram
send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
params = {
    'chat_id': chat_id,
    'text': message
}
response = requests.post(send_message_url, params=params)

if response.status_code == 200:
    print("消息发送成功")
else:
    print(f"消息发送失败，错误码：{response.status_code}")
