import requests

# Step 1: 读取现有的 api_data.txt 文件内容
file_path = 'api_data.txt'

try:
    with open(file_path, 'r') as file:
        existing_content = file.read()
except FileNotFoundError:
    existing_content = ""  # 如果文件不存在，设置为空字符串

# Step 2: 从 API 获取数据
api_url = 'https://ipdb.api.030101.xyz/?type=bestcf&country=true'
response = requests.get(api_url)

if response.status_code == 200:
    new_data = response.text
else:
    print(f"Failed to fetch data from API. Status code: {response.status_code}")
    new_data = ""

# Step 3: 更新文件内容（可以选择追加或覆盖）
# 这里是选择追加数据
updated_content = existing_content + "\n" + new_data

# Step 4: 将更新后的内容写回到 api_data.txt 文件中
with open(file_path, 'w') as file:
    file.write(updated_content)

print("File updated successfully.")
