import requests
import logging
from colorama import Fore, Style
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


def rsa_encrypt_pkcs1v15(data: str, public_key: str) -> str:
    """
    RSA 加密函数（PKCS#1 v1.5 填充）

    :param data: 待加密的明文
    :param public_key: 支持两种格式的公钥：
       1. 完整 PEM 格式（含 -----BEGIN PUBLIC KEY----- 头尾）
       2. 原始 Base64 字符串（自动添加 PEM 头尾）
    :return: Base64 编码的加密结果
    """
    # 自动补全 PEM 头尾（如果缺失）
    if not public_key.strip().startswith('-----BEGIN'):
        public_key = f'''-----BEGIN PUBLIC KEY-----
{public_key.strip()}
-----END PUBLIC KEY-----'''

    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_bytes = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()
    except (ValueError, IndexError, TypeError) as e:
        raise ValueError("无效的公钥格式") from e


def encrypt(data):
    try:
        key_url = 'https://www.baomi.org.cn/portal/main-api/getPublishKey.do'
        response = requests.get(key_url)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}获取公钥失败，状态码: {response.status_code}{Style.RESET_ALL}")
            return None

        public_key = response.json()['data']
        encrypted_data = rsa_encrypt_pkcs1v15(data, public_key)
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


if __name__ == '__main__':
    encrypt("za123456")
