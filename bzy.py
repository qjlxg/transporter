import requests
import random
import string
import warnings

warnings.filterwarnings("ignore")

# 基本信息设置
host = "www.otcopusapp.cc"  # 请替换为实际的主机地址
path = "lx3af288h5i8pz380"  # 请替换为实际路径
tg = "https://t.me/eliangwww"  # Telegram 链接，如有需要请更新

# 生成随机邮箱和密码
def generate_random_alpha_string(length=6):
    letters = string.ascii_letters + string.digits
    return "".join(random.choices(letters, k=length))

email = f"{generate_random_alpha_string()}@gmail.com"
password = f"{generate_random_alpha_string(10)}"

# 注册接口 URL（假设路径为 /api/v1/passport/auth/register）
register_url = f"https://{host}/{path}/api/v1/passport/auth/register"

# 注册数据
register_data = {
    "email": email,
    "password": password,
    "invite_code": "pXdFSnIH",  # 确保此处填写的是正确的邀请码
    "email_code": "pXdFSnIH"    # 可能需要从注册流程中获取验证码
}

# 请求头
headers = {
    "Accept": "*/*",
    "Content-Language": "zh-CN",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15148 Safari/604.1",
    "Referer": f"https://{host}/{path}/login"
}

# 使用会话进行请求
session = requests.Session()

# 尝试注册
register_response = session.post(register_url, json=register_data, headers=headers, verify=False)

if register_response.status_code == 200:
    print("注册成功！")
    register_json = register_response.json()
    print("注册账号:", email)
    print("注册密码:", password)

    # 登录接口 URL
    login_url = f"https://{host}/{path}/api/v1/passport/auth/login"

    login_data = {
        "email": email,
        "password": password
    }

    # 进行登录
    login_response = session.post(login_url, json=login_data, headers=headers, verify=False)

    if login_response.status_code == 200:
        login_json = login_response.json()
        token = login_json.get('data', {}).get('token')

        if token:
            subscribe_url = f'https://{host}/{path}/api/v1/client/subscribe?token={token}'
            print("\n注册并登录成功，订阅地址:")
            print(subscribe_url)
            print("Telegram 联系: " + tg)

            # 访问订阅链接并获取返回数据
            try:
                subscribe_response = session.get(subscribe_url, headers=headers, verify=False)

                if subscribe_response.status_code == 200:
                    # 将返回的数据保存到文件
                    with open('data/bzy.txt', 'w') as f:
                        f.write("订阅链接返回的内容:\n")
                        f.write(subscribe_response.text)  # 保存返回的文本内容
                        f.write(f"\nTelegram 联系: {tg}\n")
                    print("订阅链接的返回内容已保存到 data/bzy.txt")
                else:
                    print(f"访问订阅链接失败，状态码: {subscribe_response.status_code}")
            except Exception as e:
                print(f"访问订阅链接时发生错误: {e}")
        else:
            print("登录成功，但未获取到 token！")
    else:
        print("登录失败，状态码:", login_response.status_code)
else:
    print("注册失败，状态码:", register_response.status_code)
    print(register_response.text)
