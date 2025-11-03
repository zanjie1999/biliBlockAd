# coding=utf-8

# bilibili 屏蔽广告用户
# v1.0 zyyme 20251103

import httpx,sys,re
from sys import argv

# https://api.bilibili.com/x/space/myinfo 拷贝一下请求cookie
cookie=""

# 广告用户的uid
bl = '''

1987938455
1082814196
1919627194
1957313739
1817661914
1627242161
1859459400
1430439192
1356882480
1826766269
1926952280
2103756604
1937207796
1390190849
1935943673
2117318938
1182860491
1405481177
1479015778
1226114823
1899633480
1029014554
1256184566
1680773766
'''


csrf = ''

def headers(uid, cookie=cookie):
    return {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'cookie': cookie,
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://space.bilibili.com',
        'priority': 'u=1, i',
        'referer': 'https://space.bilibili.com/' + uid,
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

# 交互
print("屏蔽哔哩哔哩广告用户 v1.0 zyyme")
if not cookie:
    if len(argv) < 2:
        print('打开f12，访问https://api.bilibili.com/x/space/myinfo 网络里第一个请求标头里拷贝一下请求cookie\n输入cookie按回车')
        cookie = input()
    else:
        cookie = argv[1]

csrf = re.findall('bili_jct=(.+?);', cookie)[0]

d = httpx.get('https://api.bilibili.com/x/space/myinfo', headers=headers('', cookie)).json()
if 'data' in d:
    print(d['data']['name'], '粉丝数', d['data']['follower'])
else:
    print('cookie有误')
    print(d)
    input()
    sys.exit()


for uid in bl.split('\n'):
    if uid:
        print('拉黑', uid)
        d = httpx.post('https://api.bilibili.com/x/relation/modify?statistics=%7B%22appId%22:100,%22platform%22:5%7D', headers=headers(uid, cookie),
                       data="fid={}&act=5&re_src=11&gaia_source=web_main&spmid=333.1387.0.0&extend_content=%7B%22entity%22:%22user%22,%22entity_id%22:{}%7D&csrf={}".format(uid, uid, csrf)).json()
        if d.get('code') != 0:
            print(d)

print('完成')
input()



