# coding: utf8
import sys
import requests
import time

from redis import StrictRedis

redis_conn = StrictRedis(host='localhost', port=6379)

ZIROOM = 'ziroom'

while True:
    print 'start crawl %s %s ' % (sys.argv[1], str(time.time()))
    with open('ziroom.txt', 'a+') as f:
        for i in xrange(10, 9001, 10):
            payload = {'step': i, 'key_word': sys.argv[1]}
            headers = {'Referer': 'http://m.ziroom.com/BJ/search.html', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            res = requests.post('http://m.ziroom.com/list/ajax-get-data', data=payload, headers=headers)
            if 'info' in res.json()['data'] and res.json()['data']['info'] == u'\u6570\u636e\u52a0\u8f7d\u5b8c\u6bd5':
                break
            for i in res.json()['data']:
                if isinstance(i, dict) and not redis_conn.get(ZIROOM+i['id'].strip()):
                    print '%s %s %s '% (i['id'], i['title'], i['sell_price'])
                    redis_conn.set(ZIROOM+i['id'], 1)
                    f.write(str(i)+'\n')

            time.sleep(4)
    # print 'time to sleep'
    time.sleep(20*60)

