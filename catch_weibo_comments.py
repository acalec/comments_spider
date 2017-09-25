# encoding: utf-8
import json
import random

import requests

from get_ip_pool.comment_model import Comment


def get_ip():
    with open('safe_hosts.txt', 'r') as f:
        ips = list(f.readlines())
        length = len(ips) - 1
        index = random.randint(1, length)
        # print("ips[index]", ips[index])
        return ips[index]


def delete_icon(text):
    while '<span' in text and '</span>' in text:
        index_before, index_after = 0, 0
        if index_before != -1 and index_after != -1:
            index_before = text.find('<span')
            index_after = text.find('</span>')
            text = text[:index_before] + text[index_after + 7:]
    return text


def data_from_json(jsondata):
    final_data = []
    for d in jsondata:
        a = Comment()
        a.content = delete_icon(d['text'])
        a.created_at = d['created_at']
        a.commentUser = d['user']['screen_name']
        final_data.append(a)
    return len(final_data)


def get_weibo_ids(url, headers):
    weibo_ids = {}
    for i in range(1, 11):
        url = url + '&page=' + str(i)
        r = requests.get(url, headers=headers, verify=False, allow_redirects=False)
        content = r.content
        content = str(content, 'utf-8')
        jsondata = json.loads(content)
        for j in jsondata['cards']:
            weibo_ids[(j['mblog']['idstr'])] = j['mblog']['comments_count']
    return weibo_ids


def get_comments(weibo_ids, headers):
    w_ids = []
    for k, v in weibo_ids.items():
        if v != 0:
            w_ids.append(str(k))
    before_url = 'https://m.weibo.cn/api/comments/show?id='
    after_url = '&page='
    comment_count_by_data = {}
    for w_id in w_ids:
        flag = 1
        page_num = 1
        while flag:
            w_url = before_url + w_id + after_url + str(page_num)
            proxy_ip = get_ip()
            r = requests.get(w_url, headers=headers, verify=False, allow_redirects=False, proxies=proxy_ip)
            content = r.content
            content = str(content, 'utf-8')
            # print("content", content)
            jsondata = json.loads(content)
            # print("jsondata", jsondata)
            flag = int(jsondata['ok'])
            if flag == 0:
                break
            comment_count_by_data[w_id] = int(data_from_json(jsondata['data'])) + (page_num - 1) * 10
            page_num += 1
    sorted_comment_count_by_label = sorted(weibo_ids.items(), key=lambda x: x[1], reverse=True)
    sorted_comment_count_by_data = sorted(comment_count_by_data.items(), key=lambda x: x[1], reverse=True)
    print("sorted_comment_count_by_label:  ", sorted_comment_count_by_label)
    print("sorted_comment_count_by_data:   ", sorted_comment_count_by_data)


def main():
    url = 'https://m.weibo.cn/api/container/getIndex?uid=1708763410&luicode=10000011&lfid=1076031708763410&f' \
          'eaturecode=20000320&type=uid&value=1708763410&containerid=1076031708763410'
    # cookie = 'SSOLoginState=1506068230; ALF=1508660230; _T_WM=be197bc6bd470c5bf8cc2030ad0497a1; M_WEIBOCN_PARAMS=luicode%3D20000061%26lfid%3D4154774108214809%26oid%3D4154774108214809%26fid%3D1005051708763410%26uicode%3D10000011'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5' \
                '4.0.2840.98 Safari/537.36'
    headers = {
        # 'Cookie': cookie,
        'User-Agent': useragent,
    }
    get_ip()
    weibo_ids = get_weibo_ids(url, headers)

    get_comments(weibo_ids, headers)


if __name__ == '__main__':
    main()
