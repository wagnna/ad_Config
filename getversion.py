
import requests
import time
import hashlib
import hmac
import base64
import re
from requests.cookies import RequestsCookieJar
def login():
    url = "https://ad.hupu.com/user/login"
    payload = {'username': 'wangna', 'password': 'Qw123456'}
    response = requests.request("POST", url, data=payload, verify=False)
    # return response
    print(response.json())
    # 创建一个cookiejar实例
    # cookie_jar = RequestsCookieJar()
    # 将获取的cookie转化为字典
    # resd = requests.utils.dict_from_cookiejar(response.cookies)
    # print(resd)
    # 放开下面的，可查看cookie 的 key/value
    # cookie_jar.set([key for key in resd][0], resd[[key for key in resd][0]], domain='ad-cc-tst.hupu.com')
    # 向请求头中添加cookie
    # res = requests.get(url, headers, cookies=cookie_jar)
    # return logincookie
    url = "https://ad.hupu.com/admin/config_version"
    headers = {
        # 'Cookie': cookie_jar,
        'content-type': 'application/json',
    }
    res1 = requests.request("GET", url, headers=headers, cookies=response.cookies,verify=False)
    get_ver = res1.json()['data']['current_version']
    return get_ver
    print(get_ver)
if __name__ == "__main__":
    login()
