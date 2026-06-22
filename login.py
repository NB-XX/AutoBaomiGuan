import requests
import logging
import json
import time
from colorama import Fore, Style
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# 平台固定配置
SITE_ID = '95'
DEVICE_ID = 1711
LOGIN_URL = "https://www.baomi.org.cn/portal/main-api/loginInNew.do"
PUBLISH_KEY_URL = 'https://www.baomi.org.cn/portal/main-api/getPublishKey.do'
QR_TOKEN_URL = "https://www.baomi.org.cn/portal/main-api/v2/spc/getQrToken.do"
QR_CHECK_URL = "https://www.baomi.org.cn/portal/api/v2/spc/checkQrToken.do"

DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
)

# 全局共享会话，复用连接池与 cookie
session = requests.Session()


def build_headers(token=None):
    """构造请求头；传入 token 时附带 token/authToken"""
    headers = {
        'User-Agent': DEFAULT_USER_AGENT,
        'Content-Type': 'application/json',
        'siteId': SITE_ID,
    }
    if token:
        headers['token'] = token
        headers['authToken'] = token
    return headers


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
        response = session.get(PUBLISH_KEY_URL)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}获取公钥失败，状态码: {response.status_code}{Style.RESET_ALL}")
            return None

        public_key = response.json()['data']
        encrypted_data = rsa_encrypt_pkcs1v15(data, public_key)
        return encrypted_data
    except Exception as e:
        logging.error(f"{Fore.RED}加密过程出错: {e}{Style.RESET_ALL}")
        raise Exception(f"加密数据失败: {e}")


def parse_qr_token(qr_payload: str) -> str:
    try:
        payload = json.loads(qr_payload)
        qr_token = payload["params"]["qrToken"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ValueError("二维码内容缺少 qrToken") from e

    if not qr_token:
        raise ValueError("二维码内容缺少 qrToken")

    return qr_token


def get_qr_code():
    response = session.post(QR_TOKEN_URL, headers={"siteId": SITE_ID})
    if response.status_code != 200:
        raise Exception(f"获取二维码失败，状态码: {response.status_code}")

    response_data = response.json()
    try:
        qr_content = response_data["data"]["data"]
    except (KeyError, TypeError) as e:
        raise ValueError("二维码接口返回格式异常") from e

    return qr_content, parse_qr_token(qr_content)


def check_qr_login(qr_token: str) -> int:
    response = session.post(QR_CHECK_URL, params={"qrToken": qr_token})
    if response.status_code != 200:
        raise Exception(f"检查二维码登录状态失败，状态码: {response.status_code}")

    response_data = response.json()
    try:
        return int(response_data["data"]["data"])
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError("二维码登录状态接口返回格式异常") from e


def print_terminal_qr(qr_content: str) -> None:
    try:
        import qrcode
    except ImportError as e:
        raise RuntimeError("缺少 qrcode 依赖，请运行 pip install -r requirements.txt") from e

    qr = qrcode.QRCode(border=2)
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def qr_login(poll_interval: int = 3, timeout: int = 300) -> str:
    """扫码登录，超时（默认 300 秒）未确认则抛出 TimeoutError"""
    qr_content, qr_token = get_qr_code()
    print(f"{Fore.CYAN}请使用保密观 APP 扫描下方二维码登录{Style.RESET_ALL}")
    print_terminal_qr(qr_content)

    deadline = time.time() + timeout
    while True:
        if time.time() > deadline:
            raise TimeoutError(f"扫码登录超时（{timeout}秒未确认）")

        try:
            status = check_qr_login(qr_token)
        except Exception as e:
            logging.error(f"{Fore.RED}检查二维码登录状态失败: {e}{Style.RESET_ALL}")
            time.sleep(poll_interval)
            continue

        if status == 1:
            print(f"{Fore.GREEN}扫码登录成功{Style.RESET_ALL}")
            return qr_token

        if status == -1:
            print(f"{Fore.YELLOW}二维码已失效，正在刷新...{Style.RESET_ALL}")
            qr_content, qr_token = get_qr_code()
            print_terminal_qr(qr_content)
            continue

        time.sleep(poll_interval)


def login(loginName, passWord):
    try:
        payload = {
            "loginName": encrypt(loginName),
            "passWord": encrypt(passWord),
            "deviceId": DEVICE_ID,
            "deviceOs": "pc",
            "lon": 40,
            "lat": 30,
            "siteId": SITE_ID,
            "sinopec": 'false'
        }

        headers = {
            'Content-Type': 'application/json',
            'siteId': SITE_ID
        }
        response = session.post(LOGIN_URL, json=payload, headers=headers)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}登录请求失败，状态码: {response.status_code}{Style.RESET_ALL}")
            raise Exception(f"登录请求失败，状态码: {response.status_code}")

        response_data = response.json()
        token = response_data.get('token')

        # 接口无论成败都返回 token 字段（失败时为空字符串），
        # 因此必须结合 successResult / 非空 token / result 综合判断
        success = response_data.get('successResult')
        if not token or success is False or str(response_data.get('result')) == '0':
            error_obj = response_data.get('error') or {}
            error_msg = error_obj.get('errorMsg') or response_data.get('message') or '未知错误'
            logging.error(f"{Fore.RED}登录失败: {error_msg}{Style.RESET_ALL}")
            raise Exception(f"登录失败: {error_msg}")

        return token
    except Exception as e:
        logging.error(f"{Fore.RED}登录过程出错: {e}{Style.RESET_ALL}")
        raise
