# coding: utf-8

import requests
import time
import json
from db import Storage
import datetime as dt

config = {
    'min_people': 3,
    'min_worthy': 0.7,
}


def send_msg(to, content):
    wechat_api = 'http://localhost:8765/send'
    requests.get(wechat_api, params={'to': to, 'content': content})


def push_msg(content, article_id):
    print article_id
    s = Storage()
    if not s.pushed(article_id):
        s.add_push(article_id, []) # 暂时不存东西, 只用来标记
        for user in s.all_active_users():
            send_msg(user, content)


def get_real_time_data():
    ctime = int(time.time())
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5'
    }

    url = 'http://www.smzdm.com/jingxuan/json_more?timesort=' + str(ctime)
    r = requests.get(url=url, headers=headers)

    data = r.text
    return data


def type_filter(type_str):
    cates = type_str.split('/')
    if cates[0] in [u'个护化妆', u'母婴用品', u'家居家装', u'旅游出行', u'服饰鞋包', u'食品保健', u'礼品钟表']:
        return True
    return False

def worth(data):
    data = json.loads(data)
    global config
    for i in data['article_list']:
        try:
            worthy = float(i['article_worthy'])
            unworthy = float(i['article_unworthy'])
            total = worthy + unworthy
            if total >= config['min_people'] \
                    and worthy / total >= config['min_worthy'] \
                    and i["article_referrals"] != u"商家自荐" \
                    and type_filter(i['gtm']['cates_str']):
                content = '%d%% (%d:%d), %s, %s, %s' % \
                          (worthy / total * 100,
                           worthy,
                           total,
                           i['article_price'],
                           i['article_title'],
                           i['article_url'])

                push_msg(content, i['article_id'])
        except Exception as e:
            print e
            pass


if __name__ == '__main__':
    # s = Storage()
    # s.set_user('hhh', {'state': 'start'})
    # print s.all_active_users()
    now = dt.datetime.now().hour
    if now >= 8 and now <= 22:
        worth(get_real_time_data())

