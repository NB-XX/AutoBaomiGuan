import requests
import execjs
import logging
from colorama import Fore, Style

def encrypt(data):
    # 加载JavaScript代码
    try:
        with open('encrypt.js', 'r', encoding='utf-8') as file:
            js_code = file.read()

        # 初始化一个 JS 上下文
        ctx = execjs.compile(js_code)
        key_url = 'https://www.baomi.org.cn/portal/main-api/getPublishKey.do'
        response = requests.get(key_url)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}获取公钥失败，状态码: {response.status_code}{Style.RESET_ALL}")
            return None
            
        public_key = response.json()['data']
        # 调用 JavaScript 中的 encrypt 函数
        encrypted_data = ctx.call('encrypt', data, public_key)
        return encrypted_data
    except Exception as e:
        logging.error(f"{Fore.RED}加密过程出错: {e}{Style.RESET_ALL}")
        raise Exception(f"加密数据失败: {e}")


def login(loginName, passWord):
    try:
        login_url = "https://www.baomi.org.cn/portal/main-api/loginInNew.do"
        payload = {
            "loginName": encrypt(loginName),
            "passWord": encrypt(passWord),
            "deviceId": 1711,
            "deviceOs": "pc",
            "lon": 40,
            "lat": 30,
            "siteId": "95",
            "sinopec": 'false'
        }

        headers = {
            'Content-Type': 'application/json',
            'siteId': '95'
        }
        response = requests.post(login_url, json=payload, headers=headers)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}登录请求失败，状态码: {response.status_code}{Style.RESET_ALL}")
            raise Exception(f"登录请求失败，状态码: {response.status_code}")
            
        response_data = response.json()
        if 'token' not in response_data:
            error_msg = response_data.get('message', '未知错误')
            logging.error(f"{Fore.RED}登录失败: {error_msg}{Style.RESET_ALL}")
            raise Exception(f"登录失败: {error_msg}")
            
        token = response_data['token']
        return token
    except Exception as e:
        logging.error(f"{Fore.RED}登录过程出错: {e}{Style.RESET_ALL}")
        raise