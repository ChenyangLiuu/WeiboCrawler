# encoding:utf-8
import requests
import httpx
import json
from bs4 import BeautifulSoup
import time
import csv
import random
from mongo import save_to_mongo, connect_to_mongo

table_name1 = 'comments'
collection1=connect_to_mongo(table_name1)


table_name2 = 'weibo_content'
collection2=connect_to_mongo(table_name2)



keyword='书'
requests = requests.session()  # 建立一个Session

cookitext = '_T_WM=5a920360a376d10aa9f0557b02510103; SCF=Ahvp2dJs7II7hCt72nj1yHzeSLl_lYtOtWDINyx9R9wvI7-UFJNAN5C2zUx1l54S-rf3CG1bUohNlHuYYMgGN18.; SUB=_2A25Mwb4qDeRhGeNI6lYW8ybEzziIHXVsTcJirDV6PUJbktCOLVfGkW1NSIs8fSmPVzMZc1Q0hI3LmGh1KL7Dx2fM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWCjlqNGpiX0zjGV23oNRFA5JpX5K-hUgL.Fo-ceKBNe0nRShB2dJLoI7yeIPH9KK54SBtt; ALF=1642945402'

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookitext,
    'referer': 'https://weibo.com/2750621294/KAf1AFVPD',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-5b5f81f871c6ff6846bf3a92f1d5efed-1ab32a39ad75711a-00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': '7yIZGS_IPx7EteZ6TT86YYAZ',
}


def getWeiboCommentinfo(url):
    """
    主要是获取微博的信息，内容以及这个微博 MID UID,
    :param url:
    :return:
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookitext,
        'referer': 'https://www.baidu.com/link?url=79KIn7lPAsM1SqpiE6ub8unuDW2xwxX-4CyvQvA8HLS&wd=&eqid=dfbc01160004d2dc00000004619e5581',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.content, 'lxml')
    conetnt = html.find_all('div', class_="card-wrap")  # 这里CALSS 要加下划线
    for ct in conetnt:
        user_info = ct.find_all('a', class_="name")
        if user_info != []:
            try:
                mid = ct['mid']  # 获取微博ID
            except:
                pass
            else:
                user_name = user_info[0].text  # 用户名称
                uid = str(ct.find('div', class_="avator").find('a')['href']).split('/')[-1].split("?")[0]  # 获取UID
                user_index = "https:" + user_info[0]['href']  # 用户主页
                user_from = str(ct.find('p', class_="from").text).replace(' ', '').replace('\n', '')  # 时间和发布终端设备名称
                weibo_content = str(ct.find('p', class_="txt").text).replace(' ', '').replace('\n', '')  # 微博内容
                weiboContent = {}
                weiboContent['weibo_content']= weibo_content
                data = [weibo_content, user_name, user_from, user_index, mid, uid]

                max_id = 0
                htmlComment(data)
                try:
                  getCommentLevel1(data, max_id)
                except:
                    pass


def getCommentLevel1(data, max_id):
    """
    一级评论

    :return:
    """
    mid = data[-2]
    uid = data[-1]

    url = "https://weibo.com/ajax/statuses/buildComments?"

    par = {
        'id': mid,
        'is_show_bulletin': '2',
        'is_mix': '0',
        'max_id': max_id,
        'count': '20',
        'uid': uid,
    }
    client = httpx.Client(http2=True, verify=False)
    response = client.get(url, params=par, headers=headers)
    jsondata = json.loads(response.text)
    max_id = jsondata['max_id']  # 获取下一页mid
    content = jsondata['data']
    for ct in content:
        comments = {}
        created_at = ct['created_at']  # 评论时间
        comment_time = time.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')  # 评论时间
        comments['comment_time'] = time.strftime("%Y-%m-%d %H:%M:%S", comment_time)  # 评论时间
        comments['comment_text'] = ct['text_raw']  # 评论内容
        comments['comment_user'] = ct['user']['screen_name']  # 评论人名称
        print(comments['comment_text'])
        save_to_mongo(collection1, comments)

    if max_id == 0:
        pass
    else:
        getCommentLevel1(data, max_id)


def htmlComment(data):

    mid = data[-2]
    uid = data[-1]
    url = 'https://s.weibo.com/Ajax_Comment/small?'
    par = {
        'act': 'list',
        'mid': mid,
        'uid': uid,
        'smartFlag': 'false',
        'smartCardComment': '',
        'isMain': 'true',
        'pageid': 'weibo',
        '_t': '0',
    }
    client = httpx.Client(http2=True, verify=False)
    response = client.get(url, params=par, headers=headers)
    jsondata = json.loads(response.text)['data']['html']
    html = BeautifulSoup(jsondata, 'lxml')
    comment_content = html.find_all('div', class_="content")
    for cc in comment_content:
        comments={}
        comment_info = str(cc.find('div', class_='txt').text).replace('\n', '').replace(' ', '').split('：')
        comments['comment_text'] = comment_info[-1]
        comments['comment_user'] = comment_info[0]
        comments['comment_time'] = cc.find('p', class_="from").text
        print(comments['comment_text'])
        save_to_mongo(collection1, comments)


def runx(keyword):
    keytext = keyword
    n = 0
    for x in range(1, 51):
        url = f"https://s.weibo.com/weibo?q={keytext}&page={x}"

        t = random.randint(2,5)

        print(f"{t}秒后开始抓取")
        time.sleep(t)
        getWeiboCommentinfo(url)






if __name__ == '__main__':
    runx(keyword)