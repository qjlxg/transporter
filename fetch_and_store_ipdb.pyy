import requests
from datetime import datetime
import os

# Step 1: 获取API数据
api_url = "https://ipdb.api.030101.xyz/?type=bestcf&country=true"
response = requests.get(api_url)
if response.status_code == 200:
    data = response.text
else:
    raise Exception(f"API 请求失败，状态码: {response.status_code}")

# Step 2: 将数据保存为文件
filename = f"ipdb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
file_path = os.path.join("data", filename)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

with open(file_path, "w") as file:
    file.write(data)

print(f"数据已保存到 {file_path}")
