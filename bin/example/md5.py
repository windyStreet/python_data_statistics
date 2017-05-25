print(sign)
print(sign)

# response = urllib2.urlopen(url, request_data)

from urllib import request, parse

url = r'https://www.baidu.com/'

# req = urllib.request.urlopen(url)
req = urllib.request.Request(url)
print(req.read())
