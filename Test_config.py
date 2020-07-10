

import requests
import time
import hashlib
import hmac
import base64
import re
from getversion import login
houtai_ver=login()
# print(type(houtai_ver))
print("后台版本号："+str(houtai_ver))
l_config={}
def re_code():
    # import requests
    # 拼接url
    url = "http://goblin.hupu.com/3/7.5.12" \
          "/config/app?make=iPhone&client=B9F8C04E-8CB9-485A-B584-D99C4D80EC36&height=2208&model=iPhone8%2C2&os_version=12.0.1&_idfa=C4BD5BA2-6682-425F-98BF-4A94D331F736&version=&width=1242&sign=289fefd8871c210cae4e09123e94d29f&client_id=80175836"

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    req = response.json()
    code =req["code"]
    re_ver = req['data']["version"]
    ad_type_pageid = len(req['data']['ad_type'])

    l_config["code"]=code
    print(ad_type_pageid)
    l_config["7512ad_type_pageid_个数"]=ad_type_pageid
    # l_config["version"] = re_ver
    realert_ver = re_ver[0:10] + " " + re_ver[11:19]
    # 后台返回的版本号和接口返回的比对，若一致，就写字典里面值为true
    if houtai_ver == realert_ver:
        l_config["assert_version"] = True

    else:
        l_config["assert_version"] = False
        # 将两个结果插到字典里面
        l_config["houtai_version"] = houtai_ver
        l_config["version"] = re_ver

    # 把str2切割
    # print(type(str2))
    # print(str2[0:10] + " " + str2[11:19])

    # print(type(houtai_ver))

    # return len(ad_all)
    return l_config
def from_morever_adtype():
 #     把多个版本返回的adtype数放一个字典里面
     list_ver=['7.5.11','7.5.12']
     l_morever_adtype=[]
     for i in range(len(list_ver)):
        version_url=list_ver[i]
        url = "http://goblin.hupu.com/3/"+version_url+ \
           "/config/app?make=iPhone&client=B9F8C04E-8CB9-485A-B584-D99C4D80EC36&height=2208&model=iPhone8%2C2&os_version=12.0.1&_idfa=C4BD5BA2-6682-425F-98BF-4A94D331F736&version=&width=1242&sign=289fefd8871c210cae4e09123e94d29f&client_id=80175836"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        req = response.json()
        print(req['data'])
        ad_type_pageid = len(req['data']['ad_type'])
        l_morever_adtype.append(ad_type_pageid)
     print(l_morever_adtype)
     if l_morever_adtype[0]==l_morever_adtype[1]:
        l_config["l_morever_adtype"] = "adtype数量相同"
     else:
        l_config["l_morever_adtype"] = "adtype数量不同"






def SendMessage(message = ''):

    # secret：密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串，例如：SECxxxxxxxx
    secret = 'SEC42e9cea179a668cfd001d3309c08710e4d9029d3bec1cb5e19773247f5e73162'
    # access_token：创建完钉钉机器人之后会自动生成，例如：access_tokenxxxx
    access_token ="f4042504307bd013e7ad42f59320045ddbc26f72b3867d755b72147f9e27db1d"

    # timestamp：当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    timestamp = int(round(time.time() * 1000))

    # 加密，获取sign和timestamp
    data = (str(timestamp) + '\n' + secret).encode('utf-8')
    secret = secret.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, data, digestmod=hashlib.sha256).digest())
    reg = re.compile(r"'(.*)'")
    signature = str(re.findall(reg,str(signature))[0])

    # 发送信息
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&sign=%s&timestamp=%s' % (access_token,signature,timestamp)
    # url ="https://oapi.dingtalk.com/robot/send?access_token=f4042504307bd013e7ad42f59320045ddbc26f72b3867d755b72147f9e27db1d"
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    try:
        response = requests.post(url, headers = headers, json = message, timeout = (3,60),verify=False)
        print(response)
        response_msg = str(response.status_code) + ' ' + str(response.content)
        print(response_msg)
    except Exception as error_msg:
        print('error_msg==='+str(error_msg))
        response_msg = error_msg

    return response_msg

if __name__ == "__main__":
    from_morever_adtype()
    msg = {"msgtype":"text","text":{"content":re_code()},"at":{"isAtAll":True}}   #content需要从别的地方拿到值
    # msg_adtype = {"msgtype":"text","text":{"content":re_adtype()},"at":{"isAtAll":True}}   #content需要从别的地方拿到值

    SendMessage(msg)
    # SendMessage(msg_adtype)
'''
问题：
1、两个版本判断adtype的前提条件是明确这2个版本个数一致
2、什么时候才会发预警

'''
