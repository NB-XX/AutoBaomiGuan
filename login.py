import requests
import execjs

def encrypt(data):
    # 加载JavaScript代码
    with open('encrypt.js', 'r',encoding='utf-8') as file:
        js_code = file.read()

    # 初始化一个 JS 上下文
    ctx = execjs.compile(js_code)
    key_url ='https://www.baomi.org.cn/portal/main-api/getPublishKey.do'
    response = requests.get(key_url)
    public_key = response.json()['data']
    # 调用 JavaScript 中的 encrypt 函数
    encrypted_data = ctx.call('encrypt', data, public_key)
    return encrypted_data


def login(loginName,passWord):
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

    response = requests.post(login_url, json=payload)
    token = response.json()['token']
    return token