#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import http.cookiejar
import json
import random
import time


def get_comCode(postid):
    url_xhr = "http://www.kuaidi100.com/autonumber/autoComNum?"
    req = urllib.request.Request(url_xhr)

    # deal with headers
    ori_headers = {
        'Host': 'www.kuaidi100.com',
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'DNT': '1',
        'Referer': 'http://www.kuaidi100.com/',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Origin': 'http://www.kuaidi100.com',
        'Content-Length': '0'
    }

    # deal with form data
    form_data = urllib.parse.urlencode({
        'text': postid,
    }).encode()

    # add headers to req
    for key, value in ori_headers.items():
        req.add_header(key, value)
    # deal with cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)

    op = opener.open(req, form_data)
    data_bytes=op.read()

    data_str = bytes.decode(data_bytes)

    ori_content = json.loads(data_str)
    inner_content = ori_content['auto'][0]['comCode']

    print('快递公司为'+inner_content)
    time.sleep(1)

    return inner_content


def get_content(postid):

    url_xhr = "http://www.kuaidi100.com/query?"
    req = urllib.request.Request(url_xhr)

    # deal with headers
    ori_headers = {
        'Host': 'www.kuaidi100.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://www.newrank.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Referer': 'http://www.kuaidi100.com/',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    # deal with form data
    temp = str(random.random())
    type = get_comCode(postid)
    form_data = urllib.parse.urlencode({
        'type': type,
        'postid': postid,
        'id': '1',
        'valicode': '',
        'temp': temp
    }).encode()

    # add headers to req
    for key, value in ori_headers.items():
        req.add_header(key, value)
    # deal with cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)

    op = opener.open(req, form_data)
    data_bytes=op.read()

    data_str = bytes.decode(data_bytes)

    ori_content = json.loads(data_str)
    inner_content = ori_content['data']
    return inner_content, postid


def add_postid():
    yes_or_no = input("是否有新快递单号(请输入yes or no)")
    goon = '1'
    add = 'no'
    while goon == '1':
        if yes_or_no == "yes":
            new_postid = input("请输入新快递单号")
            with open('postid.txt','a') as f:
                f.write(new_postid+'\n')
            f.close()
            print('添加完成')
            add = input('还要继续添加订单号吗 (yes or no)')
        else:
            print('结束添加')
            break
        if add == 'no':
            goon = 0
            print('结束添加')


def get_postid():
    try:
        with open('postid.txt','r') as f:
            content = f.readlines()
            f.close()
    except:
        print("无已有快递单号,请先输入快递单号")
        add_postid()
        content = get_postid()
    return content


def main():
    add_postid()
    context = get_postid()
    for x in context:
        print('加载中... ...')
        time.sleep(5)
        postid = x.strip('\n')
        print('即将查询的快递单号为 '+postid)
        try:
            content, postid = get_content(postid)
            print('单号为 '+postid+' 的快递信息为:')
            for x in content:
                print(x['time'] + x['context'])
            print('')
        except:
            print('快递单号错误')

if __name__ == '__main__':
    main()