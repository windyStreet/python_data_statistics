from urllib import request, parse
import hashlib
import json
from bin.until import Time
import urllib


def md5(data):
    m = hashlib.md5(data.encode("gb2312"))
    return m.hexdigest()


appkey = '59228348f43e483a3a00114a'
app_master_secret = 'qhf9uszyys1nbv55vf9jbkzzgubhsvkx'
timestamp = Time.getNowTimeStamp()
method = 'POST'
url = 'http://msg.umeng.com/api/send'
params = {'appkey': appkey,
          'timestamp': timestamp,
          'device_tokens': "AmDxT8OufLFvoS_afW3-_8jmP6zCy43gYUP1-6jFYWN7",
          'type': 'unicast',
          'payload': {'body': {'ticker': 'Hello World',
                               'title': 'ABC',
                               'text': 'abcdef',
                               'after_open': 'go_app'},
                      'display_type': 'notification'
                      }
          }
post_body = json.dumps(params)
sign = md5('%s%s%s%s' % (method, url, post_body, app_master_secret))
url = r'http://msg.umeng.com/api/send'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
data = {
    "sign": sign
}
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, headers=headers, data=data)
# page = request.urlopen(req).read()
code = request.urlopen(req).code
print(code)
# page = page.decode('utf-8')
